from kafka.admin.acl_resource import (ACL, ACLOperation, ACLPermissionType, ACLResourcePatternType, ResourcePattern,
                                      ResourceType)


def test_different_acls_are_different() -> None:
    one = ACL(
        principal='User:A',
        host='*',
        operation=ACLOperation.ALL,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(
            resource_type=ResourceType.TOPIC,
            resource_name='some-topic',
            pattern_type=ACLResourcePatternType.LITERAL
        )
    )

    two = ACL(
        principal='User:B',  # Different principal
        host='*',
        operation=ACLOperation.ALL,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(
            resource_type=ResourceType.TOPIC,
            resource_name='some-topic',
            pattern_type=ACLResourcePatternType.LITERAL
        )
    )

    assert one != two
    assert hash(one) != hash(two)

def test_different_acls_are_different_with_glob_topics() -> None:
    one = ACL(
        principal='User:A',
        host='*',
        operation=ACLOperation.ALL,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(
            resource_type=ResourceType.TOPIC,
            resource_name='*',
            pattern_type=ACLResourcePatternType.LITERAL
        )
    )

    two = ACL(
        principal='User:B',  # Different principal
        host='*',
        operation=ACLOperation.ALL,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(
            resource_type=ResourceType.TOPIC,
            resource_name='*',
            pattern_type=ACLResourcePatternType.LITERAL
        )
    )

    assert one != two
    assert hash(one) != hash(two)

def test_same_acls_are_same() -> None:
    one = ACL(
        principal='User:A',
        host='*',
        operation=ACLOperation.ALL,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(
            resource_type=ResourceType.TOPIC,
            resource_name='some-topic',
            pattern_type=ACLResourcePatternType.LITERAL
        )
    )

    two = ACL(
        principal='User:A',
        host='*',
        operation=ACLOperation.ALL,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(
            resource_type=ResourceType.TOPIC,
            resource_name='some-topic',
            pattern_type=ACLResourcePatternType.LITERAL
        )
    )

    assert one == two
    assert hash(one) == hash(two)
    assert len(set((one, two))) == 1
