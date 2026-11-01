import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import datetime, timezone


def _utc_now_iso():
    # Existing provenance files on disk end the stamp with "Z", so keep
    # that exact shape instead of switching to a +00:00 suffix and making
    # old and new records format differently. utcnow() itself is gone in
    # spirit (deprecated), hence now(timezone.utc).
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProvenanceRecorder:
    """
    Records the build steps (commands, versions) that created an artifact.
    Outputs a JSON provenance file that can be used to verify the artifact's lineage.
    """

    def __init__(self, artifact_path, provenance_file="provenance.json"):
        """
        Initializes the ProvenanceRecorder.

        Args:
            artifact_path (str): Path to the artifact to track.
            provenance_file (str): Name of the provenance file.
        """
        self.artifact_path = artifact_path
        self.provenance_file = provenance_file
        self.provenance_data = {
            "artifact": self.artifact_path,
            "created_at": _utc_now_iso(),
            "build_steps": [],
            "artifact_hash": None,
        }
        self.load_existing_provenance()

    def load_existing_provenance(self):
        """Loads existing provenance data if the file exists."""
        if os.path.exists(self.provenance_file):
            try:
                with open(self.provenance_file, 'r') as f:
                    self.provenance_data = json.load(f)
                # A file written by an older run may lack keys the rest of
                # the class assumes. Fill the gaps instead of failing later
                # with a KeyError far from the actual cause.
                self.provenance_data.setdefault("build_steps", [])
                self.provenance_data.setdefault("artifact_hash", None)
                # Loading replaces the fresh dict outright, which is
                # what keeps the original created_at stamp from the
                # first run instead of restamping it on every later run.
                # Only these two keys get repaired, though: a file
                # missing artifact or created_at stays missing, and
                # nothing downstream happens to read those two keys.
            except (FileNotFoundError, json.JSONDecodeError) as e:
                # Starting fresh here means the next save overwrites the
                # unreadable file without keeping a copy. For a corrupt
                # provenance file that trade loses the old record, and
                # this warning is the only trace it ever existed.
                logging.warning(f"Could not load existing provenance file: {e}. Starting fresh.")


    def add_build_step(self, command, version=None):
        """
        Adds a build step to the provenance data.

        Args:
            command (str): The command that was executed.
            version (str, optional): The version of the tool used. Defaults to None.
        """
        try:
            step = {
                "command": command,
                "executed_at": _utc_now_iso(),
            }
            # No version means no version key at all, not a null. Anyone
            # reading these files has to test for the key, and I prefer
            # that to a file full of empty fields pretending I recorded
            # something I did not.
            if version:
                step["version"] = version
            self.provenance_data["build_steps"].append(step)
            logging.info(f"Added build step: {command}")
        except Exception as e:
            logging.error(f"Error adding build step: {e}")
            raise

    def calculate_hash(self, algorithm="sha256"):
        """
        Calculates the hash of the artifact.

        Args:
            algorithm (str): The hashing algorithm to use (e.g., "sha256", "sha512"). Defaults to "sha256".
        """
        try:
            if not os.path.exists(self.artifact_path):
                raise FileNotFoundError(f"Artifact not found: {self.artifact_path}")

            hasher = hashlib.new(algorithm)
            with open(self.artifact_path, "rb") as f:
                # Chunked reads keep a multi-gigabyte artifact out of
                # memory. The digest does not depend on chunk size, so
                # 4096 is a buffer choice, not part of the record format.
                while chunk := f.read(4096):
                    hasher.update(chunk)

            self.provenance_data["artifact_hash"] = {
                "algorithm": algorithm,
                "hash": hasher.hexdigest(),
            }
            logging.info(f"Calculated {algorithm} hash: {self.provenance_data['artifact_hash']['hash']}")
        except FileNotFoundError as e:
            logging.error(f"File not found error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error calculating hash: {e}")
            raise

    def save_provenance(self):
        """
        Saves the provenance data to a JSON file.
        """
        try:
            with open(self.provenance_file, "w") as f:
                json.dump(self.provenance_data, f, indent=4)
            logging.info(f"Provenance data saved to: {self.provenance_file}")
        except Exception as e:
            logging.error(f"Error saving provenance data: {e}")
            raise


def setup_argparse():
    """
    Sets up the argument parser.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Records the build steps and hash of an artifact for provenance tracking."
    )
    parser.add_argument("artifact_path", help="Path to the artifact")
    parser.add_argument(
        "--provenance_file",
        default="provenance.json",
        help="Name of the provenance file (default: provenance.json)",
    )
    parser.add_argument(
        "--command", help="Command executed to build the artifact"
    )
    parser.add_argument("--version", help="Version of the tool used to build the artifact")
    parser.add_argument(
        "--hash_algorithm",
        default="sha256",
        help="Hashing algorithm to use (default: sha256)",
    )
    return parser


def main():
    """
    Main function.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # Input validation
        if not os.path.exists(args.artifact_path):
            raise FileNotFoundError(f"Artifact not found: {args.artifact_path}")

        recorder = ProvenanceRecorder(args.artifact_path, args.provenance_file)

        # This order matters. The step is added in memory first, the
        # hash is taken second, and the save is last, so a hashing
        # failure, say an algorithm name hashlib does not know, leaves
        # the file on disk untouched and the step is lost with the
        # process. I would rather lose the step than write a record
        # claiming a hash that was never taken.
        if args.command:
            recorder.add_build_step(args.command, args.version)

        recorder.calculate_hash(args.hash_algorithm)

        recorder.save_provenance()

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()