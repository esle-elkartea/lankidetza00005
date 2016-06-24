## SCRIPTS DE GENERACION DE IE.SQL
## * Administration and server module is an Open Source
## * system made by Attest - free software: sw-libre@attest.es

DROP DATABASE IF EXISTS `IE`;

CREATE DATABASE `IE`;;
USE `IE`;

#
# Table structure for table T_IE_CATEGORIAS
#

CREATE TABLE `T_IE_CATEGORIAS` (
  `id` int(11) NOT NULL default '0',
  `categoria` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;


#
# Table structure for table T_IE_CLIENTES
#

CREATE TABLE `T_IE_CLIENTES` (
  `id` int(11) NOT NULL default '0',
  `cliente` varchar(20) NOT NULL default '',
  `licencia` varchar(100) NOT NULL default ''
) TYPE=MyISAM;


#
# Table structure for table T_IE_FUENTES
#

CREATE TABLE `T_IE_FUENTES` (
  `id` int(11) NOT NULL auto_increment,
  `nombre` varchar(255) NOT NULL default '',
  `descripcion` varchar(255) NOT NULL default '',
  `id_categoria` int(11) NOT NULL default '0',
  `id_idioma` int(11) NOT NULL default '0',
  `num_res` int(11) NOT NULL default '0',
  `activada` tinyint(1) NOT NULL default '0',
  `incidencia` tinyint(1) NOT NULL default '0',
  `url` varchar(255) NOT NULL default '',
  `metodo` varchar(10) NOT NULL default '',
  `static_pars` text NOT NULL,
  `retornos_carro` tinyint(1) NOT NULL default '0',
  `posiciones` varchar(25) NOT NULL default '',
  `expreg` text NOT NULL,
  `operadores` varchar(12) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;


#
# Table structure for table T_IE_FUENTES_PARAMETROS
#

CREATE TABLE `T_IE_FUENTES_PARAMETROS` (
  `id_clave` bigint(20) NOT NULL auto_increment,
  `clave` varchar(255) NOT NULL default '',
  `id_fuente` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id_clave`)
) TYPE=MyISAM;


#
# Table structure for table T_IE_IDIOMAS
#

CREATE TABLE `T_IE_IDIOMAS` (
  `id` int(11) NOT NULL default '0',
  `idioma` varchar(50) NOT NULL default '',
  PRIMARY KEY  (`id`)
) TYPE=MyISAM;


#
# Table structure for table T_IE_INSTRUCCIONES
#

CREATE TABLE `T_IE_INSTRUCCIONES` (
  `id_instruccion` bigint(20) NOT NULL auto_increment,
  `id_clave` bigint(20) NOT NULL default '0',
  `operacion` varchar(50) NOT NULL default '',
  `par1` varchar(50) NOT NULL default '',
  `par2` varchar(50) default NULL,
  `par3` varchar(50) default NULL,
  `par4` varchar(50) default NULL,
  `par5` varchar(50) default NULL,
  `par6` varchar(50) default NULL,
  `par7` varchar(50) default NULL,
  PRIMARY KEY  (`id_instruccion`)
) TYPE=MyISAM;


#
# Table structure for table T_IE_LOGS_BUSQUEDAS
#

CREATE TABLE `T_IE_LOGS_BUSQUEDAS` (
  `fechahora` datetime NOT NULL default '0000-00-00 00:00:00',
  `categoria` varchar(255) NOT NULL default '',
  `fuente` varchar(255) NOT NULL default '',
  `texto` varchar(255) NOT NULL default '',
  `numres` bigint(20) NOT NULL default '0',
  `incidencia` tinyint(1) NOT NULL default '0',
  `cliente` varchar(20) NOT NULL default ''
) TYPE=MyISAM;


#
# Table structure for table T_IE_PARAMETROS
#

CREATE TABLE `T_IE_PARAMETROS` (
  `parametro` varchar(50) NOT NULL default '',
  `valor` varchar(255) NOT NULL default '',
  PRIMARY KEY  (`parametro`)
) TYPE=MyISAM;


#
# Table structure for table T_IE_USUARIOS
#

CREATE TABLE `T_IE_USUARIOS` (
  `id` int(11) NOT NULL default '0',
  `usuario` varchar(50) NOT NULL default '',
  `password` varchar(50) NOT NULL default ''
) TYPE=MyISAM;


# Insercion de maestros por defecto

INSERT INTO `T_IE_USUARIOS` (`id`, `usuario`, `password`) VALUES (1,'admin','cde');
INSERT INTO `T_IE_IDIOMAS` (`id`, `idioma`) VALUES (1,'Castellano');
INSERT INTO `T_IE_IDIOMAS` (`id`, `idioma`) VALUES (2,'Inglés');
INSERT INTO `T_IE_IDIOMAS` (`id`, `idioma`) VALUES (3,'Euskera');
INSERT INTO `T_IE_IDIOMAS` (`id`, `idioma`) VALUES (4,'Francés');
INSERT INTO `T_IE_IDIOMAS` (`id`, `idioma`) VALUES (5,'Alemán');
INSERT INTO `T_IE_IDIOMAS` (`id`, `idioma`) VALUES (6,'Italiano'); 
INSERT INTO `T_IE_CLIENTES` (`id`, `cliente`, `licencia`) VALUES (1,'webservice','cde2006');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (1,'Bibliografía Tecnológica: Patentes, Artículos, Libros');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (2,'Proyectos y Resultados de I+D');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (3,'Ofertas de Tecnología');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (4,'Tesis Doctorales');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (5,'Normativa y Regulaciones');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (6,'Noticias de Mercado y Notas de Prensa');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (7,'Conferencias y Eventos');
INSERT INTO `T_IE_CATEGORIAS` (`id`, `categoria`) VALUES (8,'Páginas Web');
INSERT INTO `T_IE_PARAMETROS` (`parametro`, `valor`) VALUES ('USER_AGENT','[Open Source IE] v1.0');
INSERT INTO `T_IE_PARAMETROS` (`parametro`, `valor`) VALUES ('TIMEOUT','20');
INSERT INTO `T_IE_PARAMETROS` (`parametro`, `valor`) VALUES ('MAX_RES_BUSQUEDA','200');
INSERT INTO `T_IE_PARAMETROS` (`parametro`, `valor`) VALUES ('THREADS_BUSQUEDA','10');
