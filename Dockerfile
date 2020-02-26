# We're using Arch Linux
FROM archlinux:latest

#
# Updating Arch
#
RUN pacman -Syu --noconfirm

#
# Installing Packages
#
RUN pacman -Sy --noconfirm \
    coreutils \
    zsh \
    base-devel \
    bzip2 \
    curl \
    gcc \
    clang \
    git \
    sudo \
    util-linux \
    libevent \
    libffi \
    libwebp \
    libxml2 \
    libxslt \
    linux \
    linux-headers \
    musl \
    neofetch \
    postgresql \
    postgresql-client \
    postgresql-libs \
    python \
    sqlite

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

#
# Clone repo and prepare working directory
#
RUN git clone 'https://github.com/HitaloKun/Hitsuki.git' /root/hitsuki
RUN mkdir /root/hitsuki/bin/
WORKDIR /root/hitsuki/

#
# Copies session and config (if it exists)
#
COPY ./sample_config.env ./config.env* /root/hitsuki/

#
# Install requirements
#
RUN pip3 install -r requirements.txt
RUN pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
CMD ["python3","-m","hitsuki"]
