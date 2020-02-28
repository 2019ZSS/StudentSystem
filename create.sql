create database school;
use school;

create table d(
	 yxh char(2) not null primary key,
	 mc varchar(30) not null,
	 dz varchar(30) not null,
	 lxdh char(8) not null
);

insert into d values('01', '计算机学院', '上大东校区三号楼', '65347567');
insert into d values('02',	'通讯学院',	'上大东校区二号楼',	'65341234');
insert into d values('03',	'材料学院',	'上大东校区四号楼',	'65347890');

use school;
create table s(
	xh char(4) not null primary key,
	xm varchar(12) not null,
	xb char(1) not null,
	csrq date not null,
	jg varchar(12) not null,
	sjhm char(11) not null,
	yxh char(2) not null,
 foreign key (yxh) references d(yxh)
);

insert into s values(1101,	'李明',	'男',	'1993-03-06',	'上海',	'13613005486',	'02');
insert into s values(1102,	"刘晓明",	'男',	'1992-12-08',	'安徽',	'18913457890',	'01'); 
insert into s values(1103,	'张颖',	'女',	'1993-01-05',	'江苏',	'18826490423',	'01');
insert into s values(1104,	'刘晶晶',	'女',	'1994-11-06',	'上海',	'13331934111',	'01'); 
insert into s values(1105,	'刘成刚',	'男',	'1991-06-07',	'上海',	'18015872567',	'01'); 
insert into s values(1106,	'李二丽',	'女',	'1993-05-04',	'江苏',	'18107620945',	'01'); 
insert into s values(1107,	'张晓峰',	'男',	'1992-08-16',	'浙江',	'13912341078',	'01'); 


use school;
create table t(
	 gh char(4) not null primary key,
	 xm varchar(15) not null,
	 xb char(1) not null, 
	 csrq date not null,
	 xl varchar(10) not null,
	 jbgz double(8, 2) not null,
	 yxh char(2) not null,
	 foreign key (yxh) references d(yxh)
);


insert into t values('0101', '陈迪茂', '男', '1973-03-06',	'副教授', 3567.00, '01');
insert into t values('0102',	'马小红',	'女',	'1972-12-08',	'讲师',	2845.00,	'01');
insert into t values('0201',	'张心颖',	'女',	'1960-01-05',	'教授',	4200.00,	'02');
insert into t values('0103',	'吴宝钢',	'男',	'1980-11-06',	'讲师',	2554.00,	'01');


use school;
create table c(
	 kh char(8) not null primary key,
	 km varchar(20) not null,
	 xf int not null default 4,
	 xs int not null default 40,
	 yxh char(2) not null,
	 foreign key (yxh) references d(yxh)
);

insert into c values('08305001',	'离散数学',	4,	40,	'01');
insert into c values('08305002',	'数据库原理',	4,	50,	'01');
insert into c values('08305003',	'数据结构',	    4,	50,	'01');
insert into c values('08305004',	'系统结构',	    6,	60,	'01');
insert into c values('08301001',	'分子物理学',	4,	40,	'03');
insert into c values('08302001',	'通信学',	3,	30,	'02');


use school;
create table O (
	xq varchar(25) not null,
	kh char(8) not null,
	gh char(4) not null,
	sksj varchar(30) not null,
	primary key (xq, kh, gh),
	foreign key (kh) references c(kh),
	foreign key (gh) references t(gh)
); 
insert into O values('2012-2013秋季',	'08305001',	 '0103',	'星期三5-8');
insert into O values('2012-2013冬季',	'08305002',	 '0101', 	'星期三1-4');
insert into O values('2012-2013冬季',	'08305002',	 '0102',	'星期三1-4');
insert into O values('2012-2013冬季',	'08305002',	 '0103',	'星期三1-4');
insert into O values('2012-2013冬季',	'08305003',	 '0102',	'星期五5-8');
insert into O values('2013-2014秋季',	'08305004',	 '0101',	'星期二1-4');
insert into O values('2013-2014秋季',	'08305001',	 '0102',	'星期一5-8');
insert into O values('2013-2014冬季',	'08302001',	 '0201',	'星期一5-8');



use school;
create table e(
	xh char(4) not null,
	xq varchar(25) not null,
	kh char(8) not null,
	gh char(4) not null,
	pscj int,
	check(pscj >= 0 and pscj < 101),
	kscj int,
	check(kscj >= 0 and kscj < 101),
	zpcj int,
	check(zpcj >= 0 and zpcj < 101),
	primary key (xh, xq, kh, gh),
	foreign key (xh) references s(xh),
	foreign key (xq) references o(xq),
	foreign key (kh) references c(kh),
	foreign key (gh) references t(gh)
);

insert into e values('1101',	'2012-2013秋季',	'08305001',	 '0103',	60,	60,	60);
insert into e values(1102,	'2012-2013秋季',	'08305001',	'0103',	87,	87,	87);
insert into e values(1102,	'2012-2013冬季',	'08305002',	'0101',	82,	82,	82);
insert into e values(1102,	'2013-2014秋季',	'08305004',	'0101',	null,	null,	null);
insert into e values(1103,	'2012-2013秋季',	'08305001',	'0103',	56,	56,	56);
insert into e values(1103,	'2012-2013冬季',	'08305002',	'0102',	75,	75,	75);
insert into e values(1103,	'2012-2013冬季',	'08305003',	'0102',	84,	84,	84);
insert into e values(1103,	'2013-2014秋季',	'08305001',	'0102',	null,	null,	null);
insert into e values(1103,	'2013-2014秋季',	'08305004',	'0101',	null,	null,	null);
insert into e values(1104,	'2012-2013秋季',	'08305001',	'0103',	74,	74,	74);
insert into e values(1104,	'2013-2014冬季',	'08302001',	'0201',	null,	null,	null);
insert into e values(1106,	'2012-2013秋季',	'08305001',	'0103',	85,	85,	85);
insert into e values(1106,	'2012-2013冬季',	'08305002',	'0103',	66,	66,	66);
insert into e values(1107,	'2012-2013秋季',	'08305001',	'0103',	90,	90,	90);
insert into e values(1107,	'2012-2013冬季',	'08305003',	'0102',	79,	79,	79);
insert into e values(1107,	'2013-2014秋季',	'08305004',	'0101',	null,	null,	null);
insert into e values(1107,	'2013-2014冬季',	'08302001',	'0201',	100,	100,	100);

create index idx1 on s(yxh asc, xm desc); 
show index from s; 
create index idx2 on c(km);
show index from e; 

create table if not exists Account(
	usr char(33) primary key,
	pwd char(33) not null
);