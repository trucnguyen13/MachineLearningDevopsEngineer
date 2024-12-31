#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    logger.info("Downloading artifact")
    local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)
    ######################

    # Drop outliers
    logger.info("Dropping outliers")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    filename = "clean_sample.csv"
    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type= str, 
        help= "the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type= str, 
        help= "the name for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type= str, 
        help= "the type for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type= str,
        help= "a description for the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type= float,
        help= "the minimum price to consider",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type= float,
        help= "the maximum price to consider",
        required=True
    )


    args = parser.parse_args()

    go(args)