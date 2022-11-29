# Using Poetry with Conda

1. Update Poetry to version >= 1.2.x
1. Set prefer-active-python to true `poetry config virtualenvs.prefer-active-python true`
1. Set `poetry config virtualenvs.in-project true`
1. Create an environment in the project `conda create -p ./.env ...`
1. Use poetry to install dependencies