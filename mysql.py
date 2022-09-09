# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, Computed, Enum, Float, Index, Integer, JSON, LargeBinary, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, ENUM, INTEGER, MEDIUMBLOB, MEDIUMTEXT, SET, SMALLINT, TEXT, TIME, TIMESTAMP, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ColumnsPriv(Base):
    __tablename__ = 'columns_priv'
    __table_args__ = {'comment': 'Column privileges'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    Db = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Table_name = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Column_name = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Column_priv = Column(SET('Select', 'Insert', 'Update', 'References'), nullable=False, server_default=text("''"))


class Component(Base):
    __tablename__ = 'component'
    __table_args__ = {'comment': 'Components'}

    component_id = Column(INTEGER, primary_key=True)
    component_group_id = Column(INTEGER, nullable=False)
    component_urn = Column(Text, nullable=False)


class Db(Base):
    __tablename__ = 'db'
    __table_args__ = {'comment': 'Database privileges'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    Db = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, index=True, server_default=text("''"))
    Select_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Insert_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Update_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Delete_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Drop_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Grant_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    References_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Index_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Alter_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_tmp_table_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Lock_tables_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_view_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Show_view_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_routine_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Alter_routine_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Execute_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Event_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Trigger_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))


class DefaultRole(Base):
    __tablename__ = 'default_roles'
    __table_args__ = {'comment': 'Default roles'}

    HOST = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    USER = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    DEFAULT_ROLE_HOST = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("'%%'"))
    DEFAULT_ROLE_USER = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))


class EngineCost(Base):
    __tablename__ = 'engine_cost'

    engine_name = Column(String(64), primary_key=True, nullable=False)
    device_type = Column(Integer, primary_key=True, nullable=False)
    cost_name = Column(String(64), primary_key=True, nullable=False)
    cost_value = Column(Float)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    comment = Column(String(1024))
    default_value = Column(Float, Computed("((case `cost_name` when _utf8mb3'io_block_read_cost' then 1.0 when _utf8mb3'memory_block_read_cost' then 0.25 else NULL end))", persisted=False))


class Func(Base):
    __tablename__ = 'func'
    __table_args__ = {'comment': 'User defined functions'}

    name = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, server_default=text("''"))
    ret = Column(TINYINT, nullable=False, server_default=text("'0'"))
    dl = Column(CHAR(128, 'utf8mb3_bin'), nullable=False, server_default=text("''"))
    type = Column(ENUM('function', 'aggregate'), nullable=False)


t_general_log = Table(
    'general_log', metadata,
    Column('event_time', TIMESTAMP(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)")),
    Column('user_host', MEDIUMTEXT, nullable=False),
    Column('thread_id', BIGINT, nullable=False),
    Column('server_id', INTEGER, nullable=False),
    Column('command_type', String(64), nullable=False),
    Column('argument', MEDIUMBLOB, nullable=False),
    comment='General log'
)


class GlobalGrant(Base):
    __tablename__ = 'global_grants'
    __table_args__ = {'comment': 'Extended global grants'}

    USER = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    HOST = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    PRIV = Column(CHAR(32), primary_key=True, nullable=False, server_default=text("''"))
    WITH_GRANT_OPTION = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))


class GtidExecuted(Base):
    __tablename__ = 'gtid_executed'

    source_uuid = Column(CHAR(36), primary_key=True, nullable=False, comment='uuid of the source where the transaction was originally executed.')
    interval_start = Column(BigInteger, primary_key=True, nullable=False, comment='First number of interval.')
    interval_end = Column(BigInteger, nullable=False, comment='Last number of interval.')


class HelpCategory(Base):
    __tablename__ = 'help_category'
    __table_args__ = {'comment': 'help categories'}

    help_category_id = Column(SMALLINT, primary_key=True)
    name = Column(CHAR(64), nullable=False, unique=True)
    parent_category_id = Column(SMALLINT)
    url = Column(Text, nullable=False)


class HelpKeyword(Base):
    __tablename__ = 'help_keyword'
    __table_args__ = {'comment': 'help keywords'}

    help_keyword_id = Column(INTEGER, primary_key=True)
    name = Column(CHAR(64), nullable=False, unique=True)


class HelpRelation(Base):
    __tablename__ = 'help_relation'
    __table_args__ = {'comment': 'keyword-topic relation'}

    help_topic_id = Column(INTEGER, primary_key=True, nullable=False)
    help_keyword_id = Column(INTEGER, primary_key=True, nullable=False)


class HelpTopic(Base):
    __tablename__ = 'help_topic'
    __table_args__ = {'comment': 'help topics'}

    help_topic_id = Column(INTEGER, primary_key=True)
    name = Column(CHAR(64), nullable=False, unique=True)
    help_category_id = Column(SMALLINT, nullable=False)
    description = Column(Text, nullable=False)
    example = Column(Text, nullable=False)
    url = Column(Text, nullable=False)


class InnodbIndexStat(Base):
    __tablename__ = 'innodb_index_stats'

    database_name = Column(String(64, 'utf8mb3_bin'), primary_key=True, nullable=False)
    table_name = Column(String(199, 'utf8mb3_bin'), primary_key=True, nullable=False)
    index_name = Column(String(64, 'utf8mb3_bin'), primary_key=True, nullable=False)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    stat_name = Column(String(64, 'utf8mb3_bin'), primary_key=True, nullable=False)
    stat_value = Column(BIGINT, nullable=False)
    sample_size = Column(BIGINT)
    stat_description = Column(String(1024, 'utf8mb3_bin'), nullable=False)


class InnodbTableStat(Base):
    __tablename__ = 'innodb_table_stats'

    database_name = Column(String(64, 'utf8mb3_bin'), primary_key=True, nullable=False)
    table_name = Column(String(199, 'utf8mb3_bin'), primary_key=True, nullable=False)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    n_rows = Column(BIGINT, nullable=False)
    clustered_index_size = Column(BIGINT, nullable=False)
    sum_of_other_index_sizes = Column(BIGINT, nullable=False)


class PasswordHistory(Base):
    __tablename__ = 'password_history'
    __table_args__ = {'comment': 'Password history for user accounts'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Password_timestamp = Column(TIMESTAMP(fsp=6), primary_key=True, nullable=False, server_default=text("CURRENT_TIMESTAMP(6)"))
    Password = Column(Text(collation='utf8mb3_bin'))


class Plugin(Base):
    __tablename__ = 'plugin'
    __table_args__ = {'comment': 'MySQL plugins'}

    name = Column(String(64), primary_key=True, server_default=text("''"))
    dl = Column(String(128), nullable=False, server_default=text("''"))


class ProcsPriv(Base):
    __tablename__ = 'procs_priv'
    __table_args__ = {'comment': 'Procedure privileges'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    Db = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Routine_name = Column(CHAR(64), primary_key=True, nullable=False, server_default=text("''"))
    Routine_type = Column(ENUM('FUNCTION', 'PROCEDURE'), primary_key=True, nullable=False)
    Grantor = Column(String(288, 'utf8mb3_bin'), nullable=False, index=True, server_default=text("''"))
    Proc_priv = Column(SET('Execute', 'Alter Routine', 'Grant'), nullable=False, server_default=text("''"))
    Timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class ProxiesPriv(Base):
    __tablename__ = 'proxies_priv'
    __table_args__ = {'comment': 'User proxy privileges'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Proxied_host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    Proxied_user = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    With_grant = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    Grantor = Column(String(288, 'utf8mb3_bin'), nullable=False, index=True, server_default=text("''"))
    Timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class ReplicationAsynchronousConnectionFailover(Base):
    __tablename__ = 'replication_asynchronous_connection_failover'
    __table_args__ = (
        Index('Channel_name', 'Channel_name', 'Managed_name'),
        {'comment': 'The source configuration details'}
    )

    Channel_name = Column(CHAR(64), primary_key=True, nullable=False, comment='The replication channel name that connects source and replica.')
    Host = Column(CHAR(255), primary_key=True, nullable=False, comment='The source hostname that the replica will attempt to switch over the replication connection to in case of a failure.')
    Port = Column(INTEGER, primary_key=True, nullable=False, comment='The source port that the replica will attempt to switch over the replication connection to in case of a failure.')
    Network_namespace = Column(CHAR(64), primary_key=True, nullable=False, comment='The source network namespace that the replica will attempt to switch over the replication connection to in case of a failure. If its value is empty, connections use the default (global) namespace.')
    Weight = Column(TINYINT, nullable=False, comment='The order in which the replica shall try to switch the connection over to when there are failures. Weight can be set to a number between 1 and 100, where 100 is the highest weight and 1 the lowest.')
    Managed_name = Column(CHAR(64), primary_key=True, nullable=False, server_default=text("''"), comment='The name of the group which this server belongs to.')


class ReplicationAsynchronousConnectionFailoverManaged(Base):
    __tablename__ = 'replication_asynchronous_connection_failover_managed'
    __table_args__ = {'comment': 'The managed source configuration details'}

    Channel_name = Column(CHAR(64), primary_key=True, nullable=False, comment='The replication channel name that connects source and replica.')
    Managed_name = Column(CHAR(64), primary_key=True, nullable=False, server_default=text("''"), comment='The name of the source which needs to be managed.')
    Managed_type = Column(CHAR(64), nullable=False, server_default=text("''"), comment='Determines the managed type.')
    Configuration = Column(JSON, comment='The data to help manage group. For Managed_type = GroupReplication, Configuration value should contain {"Primary_weight": 80, "Secondary_weight": 60}, so that it assigns weight=80 to PRIMARY of the group, and weight=60 for rest of the members in mysql.replication_asynchronous_connection_failover table.')


class ReplicationGroupConfigurationVersion(Base):
    __tablename__ = 'replication_group_configuration_version'
    __table_args__ = {'comment': 'The group configuration version.'}

    name = Column(CHAR(255), primary_key=True, comment='The configuration name.')
    version = Column(BIGINT, nullable=False, comment='The version of the configuration name.')


class ReplicationGroupMemberAction(Base):
    __tablename__ = 'replication_group_member_actions'
    __table_args__ = {'comment': 'The member actions configuration.'}

    name = Column(CHAR(255), primary_key=True, nullable=False, comment='The action name.')
    event = Column(CHAR(64), primary_key=True, nullable=False, index=True, comment='The event that will trigger the action.')
    enabled = Column(TINYINT(1), nullable=False, comment='Whether the action is enabled.')
    type = Column(CHAR(64), nullable=False, comment='The action type.')
    priority = Column(TINYINT, nullable=False, comment='The order on which the action will be run, value between 1 and 100, lower values first.')
    error_handling = Column(CHAR(64), nullable=False, comment='On errors during the action will be handled: IGNORE, CRITICAL.')


class RoleEdge(Base):
    __tablename__ = 'role_edges'
    __table_args__ = {'comment': 'Role hierarchy and role grants'}

    FROM_HOST = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    FROM_USER = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    TO_HOST = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    TO_USER = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    WITH_ADMIN_OPTION = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))


class ServerCost(Base):
    __tablename__ = 'server_cost'

    cost_name = Column(String(64), primary_key=True)
    cost_value = Column(Float)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    comment = Column(String(1024))
    default_value = Column(Float, Computed("((case `cost_name` when _utf8mb3'disk_temptable_create_cost' then 20.0 when _utf8mb3'disk_temptable_row_cost' then 0.5 when _utf8mb3'key_compare_cost' then 0.05 when _utf8mb3'memory_temptable_create_cost' then 1.0 when _utf8mb3'memory_temptable_row_cost' then 0.1 when _utf8mb3'row_evaluate_cost' then 0.1 else NULL end))", persisted=False))


class Server(Base):
    __tablename__ = 'servers'
    __table_args__ = {'comment': 'MySQL Foreign Servers table'}

    Server_name = Column(CHAR(64), primary_key=True, server_default=text("''"))
    Host = Column(CHAR(255), nullable=False, server_default=text("''"))
    Db = Column(CHAR(64), nullable=False, server_default=text("''"))
    Username = Column(CHAR(64), nullable=False, server_default=text("''"))
    Password = Column(CHAR(64), nullable=False, server_default=text("''"))
    Port = Column(Integer, nullable=False, server_default=text("'0'"))
    Socket = Column(CHAR(64), nullable=False, server_default=text("''"))
    Wrapper = Column(CHAR(64), nullable=False, server_default=text("''"))
    Owner = Column(CHAR(64), nullable=False, server_default=text("''"))


class SlaveMasterInfo(Base):
    __tablename__ = 'slave_master_info'
    __table_args__ = {'comment': 'Master Information'}

    Number_of_lines = Column(INTEGER, nullable=False, comment='Number of lines in the file.')
    Master_log_name = Column(TEXT, nullable=False, comment='The name of the master binary log currently being read from the master.')
    Master_log_pos = Column(BIGINT, nullable=False, comment='The master log position of the last read event.')
    Host = Column(VARCHAR(255), comment='The host name of the source.')
    User_name = Column(TEXT, comment='The user name used to connect to the master.')
    User_password = Column(TEXT, comment='The password used to connect to the master.')
    Port = Column(INTEGER, nullable=False, comment='The network port used to connect to the master.')
    Connect_retry = Column(INTEGER, nullable=False, comment='The period (in seconds) that the slave will wait before trying to reconnect to the master.')
    Enabled_ssl = Column(TINYINT(1), nullable=False, comment='Indicates whether the server supports SSL connections.')
    Ssl_ca = Column(TEXT, comment='The file used for the Certificate Authority (CA) certificate.')
    Ssl_capath = Column(TEXT, comment='The path to the Certificate Authority (CA) certificates.')
    Ssl_cert = Column(TEXT, comment='The name of the SSL certificate file.')
    Ssl_cipher = Column(TEXT, comment='The name of the cipher in use for the SSL connection.')
    Ssl_key = Column(TEXT, comment='The name of the SSL key file.')
    Ssl_verify_server_cert = Column(TINYINT(1), nullable=False, comment='Whether to verify the server certificate.')
    Heartbeat = Column(Float, nullable=False)
    Bind = Column(TEXT, comment='Displays which interface is employed when connecting to the MySQL server')
    Ignored_server_ids = Column(TEXT, comment='The number of server IDs to be ignored, followed by the actual server IDs')
    Uuid = Column(TEXT, comment='The master server uuid.')
    Retry_count = Column(BIGINT, nullable=False, comment='Number of reconnect attempts, to the master, before giving up.')
    Ssl_crl = Column(TEXT, comment='The file used for the Certificate Revocation List (CRL)')
    Ssl_crlpath = Column(TEXT, comment='The path used for Certificate Revocation List (CRL) files')
    Enabled_auto_position = Column(TINYINT(1), nullable=False, comment='Indicates whether GTIDs will be used to retrieve events from the master.')
    Channel_name = Column(VARCHAR(64), primary_key=True, comment='The channel on which the replica is connected to a source. Used in Multisource Replication')
    Tls_version = Column(TEXT, comment='Tls version')
    Public_key_path = Column(TEXT, comment='The file containing public key of master server.')
    Get_public_key = Column(TINYINT(1), nullable=False, comment='Preference to get public key from master.')
    Network_namespace = Column(TEXT, comment='Network namespace used for communication with the master server.')
    Master_compression_algorithm = Column(VARCHAR(64), nullable=False, comment='Compression algorithm supported for data transfer between source and replica.')
    Master_zstd_compression_level = Column(INTEGER, nullable=False, comment='Compression level associated with zstd compression algorithm.')
    Tls_ciphersuites = Column(TEXT, comment='Ciphersuites used for TLS 1.3 communication with the master server.')
    Source_connection_auto_failover = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='Indicates whether the channel connection failover is enabled.')
    Gtid_only = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='Indicates if this channel only uses GTIDs and does not persist positions.')


class SlaveRelayLogInfo(Base):
    __tablename__ = 'slave_relay_log_info'
    __table_args__ = {'comment': 'Relay Log Information'}

    Number_of_lines = Column(INTEGER, nullable=False, comment='Number of lines in the file or rows in the table. Used to version table definitions.')
    Relay_log_name = Column(TEXT, comment='The name of the current relay log file.')
    Relay_log_pos = Column(BIGINT, comment='The relay log position of the last executed event.')
    Master_log_name = Column(TEXT, comment='The name of the master binary log file from which the events in the relay log file were read.')
    Master_log_pos = Column(BIGINT, comment='The master log position of the last executed event.')
    Sql_delay = Column(Integer, comment='The number of seconds that the slave must lag behind the master.')
    Number_of_workers = Column(INTEGER)
    Id = Column(INTEGER, comment='Internal Id that uniquely identifies this record.')
    Channel_name = Column(VARCHAR(64), primary_key=True, comment='The channel on which the replica is connected to a source. Used in Multisource Replication')
    Privilege_checks_username = Column(VARCHAR(32), comment='Username part of PRIVILEGE_CHECKS_USER.')
    Privilege_checks_hostname = Column(VARCHAR(255), comment='Hostname part of PRIVILEGE_CHECKS_USER.')
    Require_row_format = Column(TINYINT(1), nullable=False, comment='Indicates whether the channel shall only accept row based events.')
    Require_table_primary_key_check = Column(Enum('STREAM', 'ON', 'OFF'), nullable=False, server_default=text("'STREAM'"), comment='Indicates what is the channel policy regarding tables having primary keys on create and alter table queries')
    Assign_gtids_to_anonymous_transactions_type = Column(Enum('OFF', 'LOCAL', 'UUID'), nullable=False, server_default=text("'OFF'"), comment='Indicates whether the channel will generate a new GTID for anonymous transactions. OFF means that anonymous transactions will remain anonymous. LOCAL means that anonymous transactions will be assigned a newly generated GTID based on server_uuid. UUID indicates that anonymous transactions will be assigned a newly generated GTID based on Assign_gtids_to_anonymous_transactions_value')
    Assign_gtids_to_anonymous_transactions_value = Column(TEXT, comment='Indicates the UUID used while generating GTIDs for anonymous transactions')


class SlaveWorkerInfo(Base):
    __tablename__ = 'slave_worker_info'
    __table_args__ = {'comment': 'Worker Information'}

    Id = Column(INTEGER, primary_key=True, nullable=False)
    Relay_log_name = Column(TEXT, nullable=False)
    Relay_log_pos = Column(BIGINT, nullable=False)
    Master_log_name = Column(TEXT, nullable=False)
    Master_log_pos = Column(BIGINT, nullable=False)
    Checkpoint_relay_log_name = Column(TEXT, nullable=False)
    Checkpoint_relay_log_pos = Column(BIGINT, nullable=False)
    Checkpoint_master_log_name = Column(TEXT, nullable=False)
    Checkpoint_master_log_pos = Column(BIGINT, nullable=False)
    Checkpoint_seqno = Column(INTEGER, nullable=False)
    Checkpoint_group_size = Column(INTEGER, nullable=False)
    Checkpoint_group_bitmap = Column(LargeBinary, nullable=False)
    Channel_name = Column(VARCHAR(64), primary_key=True, nullable=False, comment='The channel on which the replica is connected to a source. Used in Multisource Replication')


t_slow_log = Table(
    'slow_log', metadata,
    Column('start_time', TIMESTAMP(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)")),
    Column('user_host', MEDIUMTEXT, nullable=False),
    Column('query_time', TIME(fsp=6), nullable=False),
    Column('lock_time', TIME(fsp=6), nullable=False),
    Column('rows_sent', Integer, nullable=False),
    Column('rows_examined', Integer, nullable=False),
    Column('db', String(512), nullable=False),
    Column('last_insert_id', Integer, nullable=False),
    Column('insert_id', Integer, nullable=False),
    Column('server_id', INTEGER, nullable=False),
    Column('sql_text', MEDIUMBLOB, nullable=False),
    Column('thread_id', BIGINT, nullable=False),
    comment='Slow log'
)


class TablesPriv(Base):
    __tablename__ = 'tables_priv'
    __table_args__ = {'comment': 'Table privileges'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    Db = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Table_name = Column(CHAR(64, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Grantor = Column(String(288, 'utf8mb3_bin'), nullable=False, index=True, server_default=text("''"))
    Timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    Table_priv = Column(SET('Select', 'Insert', 'Update', 'Delete', 'Create', 'Drop', 'Grant', 'References', 'Index', 'Alter', 'Create View', 'Show view', 'Trigger'), nullable=False, server_default=text("''"))
    Column_priv = Column(SET('Select', 'Insert', 'Update', 'References'), nullable=False, server_default=text("''"))


class TimeZone(Base):
    __tablename__ = 'time_zone'
    __table_args__ = {'comment': 'Time zones'}

    Time_zone_id = Column(INTEGER, primary_key=True)
    Use_leap_seconds = Column(ENUM('Y', 'N'), nullable=False, server_default=text("'N'"))


class TimeZoneLeapSecond(Base):
    __tablename__ = 'time_zone_leap_second'
    __table_args__ = {'comment': 'Leap seconds information for time zones'}

    Transition_time = Column(BigInteger, primary_key=True)
    Correction = Column(Integer, nullable=False)


class TimeZoneName(Base):
    __tablename__ = 'time_zone_name'
    __table_args__ = {'comment': 'Time zone names'}

    Name = Column(CHAR(64), primary_key=True)
    Time_zone_id = Column(INTEGER, nullable=False)


class TimeZoneTransition(Base):
    __tablename__ = 'time_zone_transition'
    __table_args__ = {'comment': 'Time zone transitions'}

    Time_zone_id = Column(INTEGER, primary_key=True, nullable=False)
    Transition_time = Column(BigInteger, primary_key=True, nullable=False)
    Transition_type_id = Column(INTEGER, nullable=False)


class TimeZoneTransitionType(Base):
    __tablename__ = 'time_zone_transition_type'
    __table_args__ = {'comment': 'Time zone transition types'}

    Time_zone_id = Column(INTEGER, primary_key=True, nullable=False)
    Transition_type_id = Column(INTEGER, primary_key=True, nullable=False)
    Offset = Column(Integer, nullable=False, server_default=text("'0'"))
    Is_DST = Column(TINYINT, nullable=False, server_default=text("'0'"))
    Abbreviation = Column(CHAR(8), nullable=False, server_default=text("''"))


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': 'Users and global privileges'}

    Host = Column(CHAR(255), primary_key=True, nullable=False, server_default=text("''"))
    User = Column(CHAR(32, 'utf8mb3_bin'), primary_key=True, nullable=False, server_default=text("''"))
    Select_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Insert_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Update_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Delete_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Drop_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Reload_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Shutdown_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Process_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    File_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Grant_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    References_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Index_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Alter_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Show_db_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Super_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_tmp_table_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Lock_tables_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Execute_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Repl_slave_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Repl_client_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_view_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Show_view_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_routine_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Alter_routine_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_user_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Event_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Trigger_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_tablespace_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    ssl_type = Column(ENUM('', 'ANY', 'X509', 'SPECIFIED'), nullable=False, server_default=text("''"))
    ssl_cipher = Column(LargeBinary, nullable=False)
    x509_issuer = Column(LargeBinary, nullable=False)
    x509_subject = Column(LargeBinary, nullable=False)
    max_questions = Column(INTEGER, nullable=False, server_default=text("'0'"))
    max_updates = Column(INTEGER, nullable=False, server_default=text("'0'"))
    max_connections = Column(INTEGER, nullable=False, server_default=text("'0'"))
    max_user_connections = Column(INTEGER, nullable=False, server_default=text("'0'"))
    plugin = Column(CHAR(64, 'utf8mb3_bin'), nullable=False, server_default=text("'caching_sha2_password'"))
    authentication_string = Column(Text(collation='utf8mb3_bin'))
    password_expired = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    password_last_changed = Column(TIMESTAMP)
    password_lifetime = Column(SMALLINT)
    account_locked = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Create_role_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Drop_role_priv = Column(ENUM('N', 'Y'), nullable=False, server_default=text("'N'"))
    Password_reuse_history = Column(SMALLINT)
    Password_reuse_time = Column(SMALLINT)
    Password_require_current = Column(ENUM('N', 'Y'))
    User_attributes = Column(JSON)
