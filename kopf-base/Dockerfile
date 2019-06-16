FROM registry.fedoraproject.org/f29/s2i-base:latest

ENV PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off

RUN INSTALL_PKGS="python3 python3-devel python3-setuptools python3-pip \
        python3-virtualenv" && \
    dnf -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    dnf -y clean all --enablerepo='*'

RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    chmod g+w /etc/passwd

RUN virtualenv ${APP_ROOT} && \
    source ${APP_ROOT}/bin/activate && \
    pip install -U pip setuptools wheel && \
    pip install kopf==0.14 openshift==0.9.0a3 && \
    chown -R 1001:0 ${APP_ROOT} && \
    fix-permissions ${APP_ROOT} -P

ENV BASH_ENV="${APP_ROOT}/bin/activate" \
    ENV="${APP_ROOT}/bin/activate" \
    PROMPT_COMMAND=". ${APP_ROOT}/bin/activate"

COPY bin/ /usr/bin/
COPY s2i/ /usr/libexec/s2i

USER 1001

ENTRYPOINT [ "container-entrypoint" ]
CMD [ "/usr/libexec/s2i/run" ]
