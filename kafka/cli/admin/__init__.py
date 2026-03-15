import argparse
import json
import logging
from collections.abc import Iterable, Sequence
from pprint import pprint
from typing import Dict, Optional, Protocol, cast

from kafka.admin.client import KafkaAdminClient
from kafka.admin.types import KafkaAdminClientParams

from .cluster import ClusterSubCommand
from .configs import ConfigsSubCommand
from .consumer_groups import ConsumerGroupsSubCommand
from .log_dirs import LogDirsSubCommand
from .topics import TopicsSubCommand


def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='python -m kafka.admin',
        description='Kafka admin client',
    )
    parser.add_argument(
        '-b', '--bootstrap-servers', type=str, action='append', required=True,
        help='host:port for cluster bootstrap servers')
    parser.add_argument(
        '-c', '--extra-config', type=str, action='append',
        help='additional configuration properties for admin client')
    parser.add_argument(
        '-l', '--log-level', type=str,
        help='logging level, passed to logging.basicConfig')
    parser.add_argument(
        '-f', '--format', type=str, default='raw',
        help='output format: raw|json')
    return parser


_LOGGING_LEVELS = {'NOTSET': 0, 'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}


def build_kwargs(props: Iterable[str]) -> KafkaAdminClientParams:
    kwargs: Dict[str, object] = {}
    v: object
    for prop in props or []:
        k, v = prop.split('=')
        try:
            v = int(v)
        except ValueError:
            pass
        if v == 'None':
            v = None
        elif v == 'False':
            v = False
        elif v == 'True':
            v = True
        kwargs[k] = v
    return cast(KafkaAdminClientParams, kwargs)


class SubCommand(Protocol):

    @classmethod
    def add_subparser(cls, subparsers: object) -> None:
        ...


def run_cli(args: Optional[Sequence[str]] = None) -> int:
    parser = main_parser()
    subparsers = parser.add_subparsers(help='subcommands')
    subcommands: list[SubCommand] = [ClusterSubCommand, ConfigsSubCommand, LogDirsSubCommand,
                TopicsSubCommand, ConsumerGroupsSubCommand]
    for cmd in subcommands:
        cmd.add_subparser(subparsers)

    config = parser.parse_args(args)
    if config.log_level:
        logging.basicConfig(level=_LOGGING_LEVELS[config.log_level.upper()])
    if config.format not in ('raw', 'json'):
        raise ValueError('Unrecognized format: %s' % config.format)
    logger = logging.getLogger(__name__)

    kwargs = build_kwargs(config.extra_config)
    kwargs['bootstrap_servers'] = config.bootstrap_servers
    client = KafkaAdminClient(**kwargs)
    try:
        result = config.command(client, config)
        if config.format == 'raw':
            pprint(result)
        elif config.format == 'json':
            print(json.dumps(result))
        return 0
    except AttributeError:
        parser.print_help()
        return 2
    except Exception:
        logger.exception('Error!')
        return 1


# Commands TODO:
    # [acls]
    # describe
    # create
    # delete

    # [configs]
    # alter
    # IncrementalAlterConfigs (not supported yet)

    # [partitions]
    # create
    # alter-reassignments (AlterPartitionReassignments - not supported yet)
    # list-reassignments (ListPartitionReassignments - not supported yet)

    # [records]
    # delete

    # [consumer-groups]
    # remove-members (not supported yet)
    # delete-offsets (not supported yet)
    # alter-offsets (not supported yet)

    # [offsets]
    # list (not supported yet)
    # delete (OffsetDelete - not supported yet)

    # leader-election
    # perform_leader_election

    # [log-dirs]
    # describe (currently broken)
    # alter (AlterReplicaLogDirs - not supported yet)

    # [client-quotas]
    # describe (DescribeClientQuotas - not supported yet)
    # alter (AlterClientQuotas - not supported yet)

    # DescribeQuorum (not supported yet)

    # [producers]
    # describe (DescribeProducers - not supported yet)

    # [transactions]
    # describe (DescribeTransactions - not supported yet)
    # list (ListTransactions - not supported yet)
    # abort (not supported yet)

    # [topics]
    # describe-partitions (DescribeTopicPartitions - not supported yet)

    # [cluster]
    # describe-features (DescribeFeatures - not supported yet)
    # update-features (UpdateFeatures - not supported yet)
    # version
    # api-versions



