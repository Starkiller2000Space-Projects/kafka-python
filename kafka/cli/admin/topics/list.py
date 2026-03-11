class ListTopics:

    @classmethod
    def add_subparser(cls, subparsers) -> None:
        parser = subparsers.add_parser('list', help='List Kafka Topics')
        parser.set_defaults(command=lambda cli, _args: cli.list_topics())
