FROM gitpod/workspace-full

USER gitpod

RUN sudo apt-get update
RUN sudo apt-get install -q -y libffi-dev python3-dev
RUN sudo rm -rf /var/lib/apt/lists/*

ENV PIPENV_VERBOSITY=-1