# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from typing import List
from sqlalchemy import Column, Computed, DateTime, Enum, ForeignKeyConstraint, Index, JSON, String, Text, text  # noqa: F401
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT, VARCHAR
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped  # noqa: F811
# sqlacodegen_v2 --generator declarative mysql+pymysql://root:shtm2023@192.168.10.222:3306/platform --tables common_query

Base = declarative_base()


class CommonQuery(Base):
    __tablename__ = 'common_query'
    __table_args__ = {'comment': '通用-查询（只对外项目提供服务 不对自身）'}

    sqlid = mapped_column(String(36), primary_key=True, comment='类型_功能_子功能')
    project = mapped_column(Enum('GRASP', 'DH', 'PTS', 'YM'), nullable=False, comment='项目')
    sql_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='SQL名称')
    sql_context = mapped_column(Text, nullable=False, comment='SQL内容')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='备注说明')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class CtPermission2button(Base):
    __tablename__ = 'ct_permission2button'
    __table_args__ = {'comment': '对照-权限按钮'}

    permission_code = mapped_column(String(36), primary_key=True, nullable=False, comment='权限码')
    menu_code = mapped_column(String(36), primary_key=True, nullable=False, comment='菜单码')
    button_code = mapped_column(Enum('add', 'edit', 'audit', 'cancel', 'export', 'del'), primary_key=True, nullable=False, server_default=text("'add'"), comment='按钮码')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class CtPermission2menu(Base):
    __tablename__ = 'ct_permission2menu'
    __table_args__ = {'comment': '对照-权限菜单'}

    permission_code = mapped_column(String(36), primary_key=True, nullable=False, comment='权限码')
    menu_code = mapped_column(String(36), primary_key=True, nullable=False, comment='菜单码')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class CtPermission2role(Base):
    __tablename__ = 'ct_permission2role'
    __table_args__ = {'comment': '对照-权限角色'}

    permission_code = mapped_column(String(36), primary_key=True, nullable=False, comment='权限码')
    role_code = mapped_column(String(36), primary_key=True, nullable=False, comment='角色码')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class CtUser2dept(Base):
    __tablename__ = 'ct_user2dept'
    __table_args__ = {'comment': '对照-用户部门'}

    userid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='用户ID')
    deptid = mapped_column(String(36), primary_key=True, nullable=False, comment='部门ID')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class CtUser2role(Base):
    __tablename__ = 'ct_user2role'
    __table_args__ = {'comment': '对照-用户角色'}

    userid = mapped_column(BIGINT(20), primary_key=True, nullable=False, comment='用户ID')
    role_code = mapped_column(String(36), primary_key=True, nullable=False, comment='角色码')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class LogAuthLogin(Base):
    __tablename__ = 'log_auth_login'
    __table_args__ = {'comment': '日志-登录'}

    userid = mapped_column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='用户ID')
    code_from = mapped_column(String(36), nullable=False, server_default=text("''"), comment='来源代码')
    id = mapped_column(INTEGER(11), primary_key=True, comment='自增序号')
    parm_json = mapped_column(JSON, comment='JSON参数')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class LogCommonQuery(Base):
    __tablename__ = 'log_common_query'
    __table_args__ = {'comment': '日志-通用查询'}

    sqlid = mapped_column(String(36), nullable=False, server_default=text("''"), comment='SQLID')
    userid = mapped_column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='用户ID')
    id = mapped_column(INTEGER(18), primary_key=True, comment='自增序号')
    parm_json = mapped_column(JSON, comment='JSON参数')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class LogCommonRedis(Base):
    __tablename__ = 'log_common_redis'
    __table_args__ = {'comment': '日志-通用缓存'}

    redis_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='缓存名称')
    userid = mapped_column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='用户ID')
    id = mapped_column(INTEGER(11), primary_key=True, comment='自增序号')
    parm_json = mapped_column(JSON, comment='JSON参数')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class LogDef(Base):
    __tablename__ = 'log_def'
    __table_args__ = {'comment': '日志-默认'}

    threadid = mapped_column(String(36), nullable=False, server_default=text("''"), comment='用户ID')
    thread_name = mapped_column(String(255), nullable=False, server_default=text("''"), comment='SQLID')
    id = mapped_column(INTEGER(11), primary_key=True, comment='自增序号')
    parm_json = mapped_column(JSON, comment='JSON参数')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class LogPostJob(Base):
    __tablename__ = 'log_post_job'
    __table_args__ = {'comment': '日志-JOB推送'}

    jobid = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='任务ID')
    userid = mapped_column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='用户ID')
    id = mapped_column(INTEGER(11), primary_key=True, comment='自增序号')
    parm_json = mapped_column(JSON, comment='JSON参数')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class MdmBra(Base):
    __tablename__ = 'mdm_bra'
    __table_args__ = {'comment': '主数据-门店信息'}

    braid = mapped_column(INTEGER(11), primary_key=True, comment='门店ID')
    bra_name = mapped_column(String(30), nullable=False, comment='门店名称')
    bra_sname = mapped_column(String(30), nullable=False, server_default=text("''"), comment='门店简称')
    bra_typeid = mapped_column(TINYINT(4), nullable=False, comment='门店类型ID')
    city = mapped_column(String(36), nullable=False, server_default=text("''"), comment='门店归属城市')
    city_code = mapped_column(String(36), nullable=False, server_default=text("''"), comment='城市代码')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='生效标记')
    bra = mapped_column(String(36), Computed("(concat(`braid`,' ',`bra_sname`))", persisted=False), comment='门店')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class MdmCate(Base):
    __tablename__ = 'mdm_cate'
    __table_args__ = {'comment': '主数据-品类群'}

    purid = mapped_column(INTEGER(11), nullable=False, comment='采购组ID')
    cateid = mapped_column(INTEGER(11), primary_key=True, comment='品类群ID')
    cate_name = mapped_column(String(36), nullable=False, comment='品类群名称')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='生效标记')
    cate = mapped_column(String(36), Computed("(concat(`cateid`,' ',`cate_name`))", persisted=False), comment='品类群')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class MdmDept(Base):
    __tablename__ = 'mdm_dept'
    __table_args__ = {'comment': '主数据-部门表'}

    deptid = mapped_column(INTEGER(11), primary_key=True, comment='部门序号')
    parentid = mapped_column(INTEGER(11), nullable=False, comment='上级部门')
    dept_name = mapped_column(String(36), nullable=False, comment='部门名称')
    ancestors = mapped_column(String(255), nullable=False, comment='祖级列表')
    flow_no = mapped_column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='排序')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='标记')
    dept = mapped_column(String(255), Computed("(concat(`deptid`,' ',`dept_name`))", persisted=False), comment='部门')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))


class MdmPur(Base):
    __tablename__ = 'mdm_pur'
    __table_args__ = {'comment': '主数据-采购组'}

    purid = mapped_column(INTEGER(11), primary_key=True, comment='采购组ID')
    pur_name = mapped_column(String(30), nullable=False, comment='采购组名称')
    divid = mapped_column(INTEGER(11), nullable=False, comment='处ID')
    div_name = mapped_column(String(30), nullable=False, comment='处名称')
    sid = mapped_column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='生效标记')
    pur = mapped_column(String(36), Computed("(concat(`purid`,' ',`pur_name`))", persisted=False), comment='采购组')
    div = mapped_column(String(36), Computed("(concat(`divid`,' ',`div_name`))", persisted=False), comment='处')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时 间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class MdmUser(Base):
    __tablename__ = 'mdm_user'
    __table_args__ = {'comment': '主数据-用户表'}

    userid = mapped_column(BIGINT(18), primary_key=True, comment='用户序号 默认手机号')
    user_name = mapped_column(String(36), nullable=False, comment='用户名称')
    nick_name = mapped_column(String(36), nullable=False, server_default=text("''"), comment='昵称')
    gender = mapped_column(Enum('male', 'female'), nullable=False, comment='男女')
    url_avatar = mapped_column(String(255), nullable=False, server_default=text("''"), comment='头像地址')
    sid = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='环境标识 0不生效 1生产 2测试 3 假删除 5本机')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最近更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class MetaDict(Base):
    __tablename__ = 'meta_dict'
    __table_args__ = {'comment': '元数据-枚举'}

    term_en = mapped_column(String(36), primary_key=True, nullable=False, comment='术语EN')
    term_key = mapped_column(TINYINT(4), primary_key=True, nullable=False, comment='键')
    term_value = mapped_column(String(36), nullable=False, comment='值')
    ldt = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更新时间')
    enum = mapped_column(String(255), Computed("(concat(`term_en`,'_',`term_key`))", persisted=False), comment='枚举主键')
    term = mapped_column(String(64), Computed("(concat(`term_key`,' ',`term_value`))", persisted=False), comment='术语')


class MetaTable(Base):
    __tablename__ = 'meta_table'
    __table_args__ = {'comment': '元数据-平台表注册'}

    table_name = mapped_column(String(36), primary_key=True, comment='表名')
    istruncate = mapped_column(Enum('Y', 'N'), nullable=False, server_default=text("'N'"), comment='是否可清空')
    remark = mapped_column(String(36), nullable=False, server_default=text("''"), comment='备注')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class MetaTag(Base):
    __tablename__ = 'meta_tag'
    __table_args__ = {'comment': '元数据-标签枚举'}

    key = mapped_column(String(36), primary_key=True, nullable=False, comment='查询KEY')
    value = mapped_column(String(36), primary_key=True, nullable=False, comment='键')
    label = mapped_column(String(36), nullable=False, comment='值')
    remark = mapped_column(String(36), nullable=False, server_default=text("''"), comment='备注')
    tag_code = mapped_column(String(64), Computed("(concat(`key`,'_',`value`))", persisted=False), comment='码')
    tag = mapped_column(String(36), Computed("(concat(`value`,' ',`label`))", persisted=False), comment='标签')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')


class MetaTerm(Base):
    __tablename__ = 'meta_term'
    __table_args__ = (
        Index('ix_reg_term_cn', 'term_cn', unique=True),
        {'comment': '元数据-字段术语'}
    )

    term_en = mapped_column(String(32), primary_key=True, comment='术语英文')
    term_cn = mapped_column(String(32), nullable=False, comment='术语中文')
    col_type = mapped_column(Enum('VC36', 'INT', 'D2', 'D3', 'BIGINT', 'TINYINT', 'DATE', 'DATETIME', 'YN', 'VARCHAR', 'D186', 'JSON'), nullable=False, comment='字段类型')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='术语的含义和使用场景等描述，不超过256字符。')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新日期')

    ct_field_cjy: Mapped[List['CtFieldCjy']] = relationship('CtFieldCjy', uselist=True, back_populates='meta_term')
    ct_field_qweather: Mapped[List['CtFieldQweather']] = relationship('CtFieldQweather', uselist=True, back_populates='meta_term')
    ct_field_sinan: Mapped[List['CtFieldSinan']] = relationship('CtFieldSinan', uselist=True, back_populates='meta_term')


class MetaWordroot(Base):
    __tablename__ = 'meta_wordroot'
    __table_args__ = {'comment': '元数据-缩写规则'}

    type = mapped_column(Enum('CLASS', 'DEPT', 'FIELD', 'PROJECT', 'RANGE', 'SOFT', ''), nullable=False, comment='类型')
    word_root_abbreviation = mapped_column(String(12), primary_key=True, comment='\t\r\n词根的缩写，如：amt。不超过12字 符。')
    word_root_full_name = mapped_column(String(64), nullable=False, comment='词根的全称，如：amount。不超过64字符。')
    word_root = mapped_column(String(128), nullable=False, comment='词根的任务名称，如：金额。不超过128字符')
    remark = mapped_column(String(255), nullable=False, comment='可添加词根含义和使用场景等描述，不超过256字符。')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新日期')


class SetGlobal(Base):
    __tablename__ = 'set_global'
    __table_args__ = {'comment': '设置-全局配置表'}

    project_name = mapped_column(Enum('GLOBAL'), primary_key=True, nullable=False, comment='项目名')
    project_key = mapped_column(Enum('SETUP'), primary_key=True, nullable=False, comment='项目 配置主键 SETUP项目配置 DDL 数据库语言')
    json_values = mapped_column(JSON, nullable=False, comment='配置值JSON')
    description = mapped_column(String(255), nullable=False, server_default=text("''"), comment='配置值说明')
    remark = mapped_column(String(255), nullable=False, server_default=text("''"), comment='备注')
    ldt = mapped_column(DateTime, comment='最近更新时间')


class SetMenu(Base):
    __tablename__ = 'set_menu'
    __table_args__ = {'comment': '设置-菜单'}

    menu_code = mapped_column(String(36), primary_key=True, comment='菜单ID')
    parent_code = mapped_column(String(36), nullable=False, server_default=text("'0'"), comment='父菜单ID')
    menu_name = mapped_column(String(255), nullable=False, comment='菜单标题')
    path = mapped_column(String(255), nullable=False, comment='菜单路径')
    redirect = mapped_column(String(255), nullable=False, server_default=text("''"), comment='重定向地址')
    component = mapped_column(String(255), nullable=False, server_default=text("''"), comment='视图文件路径')
    link = mapped_column(String(255), nullable=False, comment='外链')
    icon = mapped_column(String(255), nullable=False, server_default=text("''"), comment='菜单图标')
    keep_alive = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='是否缓存')
    affix = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='是否固定在 tabs nav')
    hide = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='是否隐藏')
    full = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='是否全屏(示例：数据大屏页面)')
    flow_no = mapped_column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='排序')
    visible = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='0不显示 1显示')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class SetPermission(Base):
    __tablename__ = 'set_permission'
    __table_args__ = {'comment': '设置-权限表'}

    permission_code = mapped_column(String(36), primary_key=True, comment='权限码')
    permission_name = mapped_column(String(36), comment='权限名称')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class SetRole(Base):
    __tablename__ = 'set_role'
    __table_args__ = {'comment': '设置-角色'}

    role_code = mapped_column(String(36), primary_key=True, comment='角色码（英文数字）')
    role_name = mapped_column(String(36), comment='角色名称')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')
    cdt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class CtFieldCjy(Base):
    __tablename__ = 'ct_field_cjy'
    __table_args__ = (
        ForeignKeyConstraint(['term_en'], ['meta_term.term_en'], onupdate='CASCADE', name='ct_field_cjy_ibfk_1'),
        Index('_fk', 'term_en'),
        {'comment': '对照-字段-创纪云'}
    )

    field = mapped_column(VARCHAR(30), primary_key=True, comment='字段')
    term_en = mapped_column(String(32), nullable=False, comment='术语')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')

    meta_term: Mapped['MetaTerm'] = relationship('MetaTerm', back_populates='ct_field_cjy')


class CtFieldQweather(Base):
    __tablename__ = 'ct_field_qweather'
    __table_args__ = (
        ForeignKeyConstraint(['term_en'], ['meta_term.term_en'], onupdate='CASCADE', name='_fk'),
        Index('_fk', 'term_en'),
        {'comment': '对照-字段-天气'}
    )

    field = mapped_column(VARCHAR(30), primary_key=True, comment='字段')
    term_en = mapped_column(String(32), nullable=False, comment='术语')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')

    meta_term: Mapped['MetaTerm'] = relationship('MetaTerm', back_populates='ct_field_qweather')


class CtFieldSinan(Base):
    __tablename__ = 'ct_field_sinan'
    __table_args__ = (
        ForeignKeyConstraint(['term_en'], ['meta_term.term_en'], onupdate='CASCADE', name='ct_field_sinan_ibfk_1'),
        Index('_fk', 'term_en'),
        {'comment': '对照-字段-司南数仓'}
    )

    field = mapped_column(VARCHAR(30), primary_key=True, comment='字段')
    term_en = mapped_column(String(32), nullable=False, comment='术语')
    ldt = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='最后更 新时间')

    meta_term: Mapped['MetaTerm'] = relationship('MetaTerm', back_populates='ct_field_sinan')

# # 连接数据库
# DATABASE_URL = "mysql+pymysql://root:shtm2022@192.168.200.174:3306/grasp"
# engine = create_engine(DATABASE_URL, echo=True)
 
# # 创建会话
# Session = sessionmaker(bind=engine)
# session = Session()
 
# # 创建所有表
# Base.metadata.create_all(engine)
    