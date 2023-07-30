import environ

env = environ.Env(PUBLIC_FACING=bool)

SET_A_ENV_VARIABLE = env.bool("WHATEVER")
