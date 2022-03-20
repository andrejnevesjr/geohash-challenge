import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from utils.pipeline import Pipeline
from utils.stdout_message import StdoutMessage


def stuart_pipeline(landing_path: str, raw_path: str) -> None:
    """Run end to end pipeline
    """
    start_time = datetime.now()
    pipeline = Pipeline()
    StdoutMessage.generic_output(2)
    pre_execution = pipeline.prepare_pipeline(landing_path, raw_path)
    if pre_execution:
        StdoutMessage.generic_output(3)
        pipeline_status = pipeline.run_pipeline(raw_path)
        if pipeline_status:
            StdoutMessage.generic_output(4)
    else:
        print("No file is available to run the pipeline")

    job_time_running = datetime.now() - start_time
    print("Challenge Elapsed Time => " + str(job_time_running))


def main():
    StdoutMessage.generic_output(1)
    landing_path = "landing"
    raw_path = "raw"
    stuart_pipeline(landing_path, raw_path)


if __name__ == '__main__':
    main()
