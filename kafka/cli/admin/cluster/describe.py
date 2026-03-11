class DescribeCluster:

    @classmethod
    def add_subparser(cls, subparsers) -> None:
        parser = subparsers.add_parser('describe', help='Describe Kafka Cluster')
        parser.set_defaults(command=lambda cli, _args: cli.describe_cluster())
