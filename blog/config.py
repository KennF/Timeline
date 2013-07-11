class Config(object):
	MONGODB_SETTINGS = {'DB' : "my_tumble_log"}
	SECRET_KEY = '\xe0_LR\x93\x81\xed]_\x0e\x1d\x86N\xfa\xd1\xce\xdbil\xce\x84}\xf2#'
	DEBUG = True

class ProductionConfig(Config):
	pass

class DevConfig(Config):
	pass
