FROM centos:7
MAINTAINER Dan Burkland <dburkland@dburkland.com>
ENV container docker

RUN rpm --import https://packages.microsoft.com/keys/microsoft.asc
RUN sh -c 'echo -e "[azure-cli]\nname=Azure CLI\nbaseurl=https://packages.microsoft.com/yumrepos/azure-cli\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/azure-cli.repo'
RUN yum -y install http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
RUN yum -y install -y awscli azure-cli bind-utils git wget openssh-client python unzip python python2-boto python-dateutil python2-pip python-keyczar python2-pyvmomi
RUN yum -y install https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.7.5-1.el7.ans.noarch.rpm
RUN yum -y update
RUN pip install --upgrade pip

RUN mkdir /etc/ansible/playbooks /etc/terraform /nmsdk /github /netapp /netapp/.git
RUN sed -i 's/#host_key_checking/host_key_checking/g' /etc/ansible/ansible.cfg
RUN git clone https://github.com/jeorryb/netapp-ansible.git /github
#RUN cd /netapp; git clone -b current https://github.com/NetApp/ansible.git
#RUN cd /netapp/ansible
#RUN git checkout mvp1
WORKDIR /etc/ansible/playbooks
COPY netapp-manageability-sdk-*.zip /root/nmsdk.zip
RUN unzip /root/nmsdk.zip -d /root/nmsdk
RUN mv /root/nmsdk/netapp-manageability-sdk-*/* /nmsdk/
RUN mkdir /github/db_library /github/db_module_utils
COPY db_library/* /github/db_library/
COPY db_module_utils/* /github/db_module_utils/
RUN cp /github/library/* /usr/lib/python2.7/site-packages/ansible/modules/storage/netapp/
RUN cp /github/module_utils/ntap_util.py /usr/lib/python2.7/site-packages/ansible/module_utils/
RUN cp -f /github/db_library/* /usr/lib/python2.7/site-packages/ansible/modules/storage/netapp/
RUN cp -f /github/db_module_utils/ntap_util.py /usr/lib/python2.7/site-packages/ansible/module_utils/
#RUN cp -f /netapp/ansible/lib/ansible/modules/storage/netapp/* /usr/lib/python2.7/site-packages/ansible/modules/storage/netapp/
#RUN cp -f /netapp/ansible/lib/ansible/module_utils/netapp.py /usr/lib/python2.7/site-packages/ansible/module_utils/
RUN rm -rf /root/nmsdk* /github /netapp
RUN pip install NetApp-Lib
RUN mkdir /root/.ssh/
#COPY id_rsa* /root/.ssh/
#RUN chmod 600 /root/.ssh/id_rsa
COPY terraform_*.zip /root/terraform.zip
RUN unzip /root/terraform.zip -d /usr/local/bin/
RUN curl -LO https://github.com/rancher/rke/releases/download/v0.1.14/rke_linux-amd64
RUN chmod +x rke_linux-amd64
RUN mv rke_linux-amd64 /usr/local/bin/rke
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x kubectl
RUN mv kubectl /usr/local/bin/
RUN mkdir /root/helm
COPY helm-*.tar.gz /root/helm.tar.gz
RUN tar xvf /root/helm.tar.gz -C /root/helm/
RUN mv /root/helm/linux-amd64/helm /usr/local/bin/
RUN rm -rvf /root/helm*

ENV PYTHONPATH /nmsdk/lib/python/NetApp:$PYTHONPATH

#ENTRYPOINT ["ansible-playbook"]