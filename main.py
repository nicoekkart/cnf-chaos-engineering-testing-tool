import argparse
from chaos import Chaos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run chaos experiments on a NSM helm installation')
    parser.add_argument('config_file')
    args = parser.parse_args()

    chaos_runner = Chaos(config_file=args.config_file)
    chaos_runner.run()