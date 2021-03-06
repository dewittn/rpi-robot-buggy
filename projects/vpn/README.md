# Remote controlling your buggy with a VPN

⚠️ **Disclaimer:** This tutorial is still a work in progress and may need some editing for clarity.

---
In honor of NASA's Perseverance rover landing on Mars, my student and I wanted to try remote controlling a buggy thousands of miles aways. To do this, we will need to install a VPN on both the Buggy Pi, and the Controller Pi. An optional step is to setup a public server that can act as a go between.
We will also a need a server that is connected to the internet host the VPN and send signals back and forth. 

I use Linode as my hosting provider. They have very affordable plans start at $5/month.

In this tutorial we will be installing, and setting the WireGuard VPN on Raspberry Pi OS. I like WireGuard because it is very fast, and relatively simple to get setup.

(Hat Tip to [Michel Deslierres](https://sigmdel.ca/michel/ha/wireguard/wireguard_02_en.html) his instructions on how to get this working, which I have simplified below.)

## Step 1: Update System

Before we install WireGuard we want to make sure our system is up to date by running the following commands.

```
sudo apt update 
sudo apt upgrade -y
```

## Step 2: Install WireGuard

As of March 2021, WireGuard is not yet part of the main Raspberry Pi OS repository. However, it is included in the `Testing` repository, which we can add with this command.

```
echo "deb http://archive.raspbian.org/raspbian testing main" | sudo tee --append /etc/apt/sources.list.d/testing.list
```

Then, we need to update the system again before installing WireGuard.

```
sudo apt update
sudo apt install wireguard
```

## Step 3: Create WireGuard Keys

```
umask 077
wg genkey > controller.privatekey
wg pubkey < controller.privatekey > controller.publickey
```

You could also run it as one command like this:
```
wg genkey | tee controller.privatekey | wg pubkey > controller.publickey
```

You will need to run the same command(s) on your Buggy Pi
```
umask 077
wg genkey | tee buggy.privatekey | wg pubkey > buggy.publickey
```

## Step 4: Set up WireGuard Server

To connect Raspberry Pi's running on different networks we need to access to a server that is connected to the public internet. If you don't have access to a public server then you can still finish this project by setting up the Controller Pi as the server.

Setting up a public server is outside the scope of this project, but here is a [Linode guide](https://www.linode.com/docs/guides/set-up-wireguard-vpn-on-ubuntu/) on how to install WireGuard on an Ubuntu server.

Once you have logged into your sever you need to generate keys. If you are using the controller as the server you can skip this step.

```
umask 077
wg genkey | tee server.privatekey | wg pubkey > server.publickey
```

Next we need to setup the configuration file, `/etc/wireguard/wg0.conf`, for the Sever. Each device on our VPN will get it's own IP address. Our routing table looks something like this:

```
192.168.2.1 # For the Public server or the Controller Pi
192.168.2.2 # For the Buggy Pi
192.168.2.3 # For the Conroller if we have a public server.
```

The server conf will look something like this.
```
[Interface]
PrivateKey = <Server Private Key>
Address = 192.168.3.1/32
SaveConfig = true
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE; ip6tables -A FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE; ip6tables -D FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
ListenPort = 51820

[Peer]
PublicKey = <Buddy Public Key>
AllowedIPs = 192.168.3.2/24

## Do not add this block if the Controller is the Server
[Peer]
PublicKey = <Controller Public Key>
AllowedIPs = 192.168.3.3/24
```

**Note:**
`<Buddy Public Key>` is just a place holder. You will need to replace it with the actual contents of the `buggy.publickey` file. The key files are just plain text and can be opened in any text editor or by running the following command.


```
$ cat buggy.publickey
7lTo3CyQ/5SJgxGgtHyWVwgAKmbIuzQhPt4L6z1ZqlY=
```

Look at [buggy-sample.conf](projects/vpn/buggy-sample.conf),  [controller-sample.conf](projects/vpn/controller-sample.conf), and [server-sample.conf](projects/vpn/server-sample.conf) for complete examples. **These are just examples. Do not use them for your project because they will not work.**

## Step 5: Setup WireGuard Client(s)

Next we need to setup the WireGuard configuration file on both the controller pi, and the buggy pi. For a more detailed explanation on how setting up the WireGuard conf check out their website. 


To get your private key you can open `controller.privatekey` in a text editor or run this command `cat controller.privatekey` you should see a string of random letters and numbers like this:
```
$ cat controller.privatekey
kHE9qqbeloFxKaHOmhd0kuDhShGx5r2e45rtB9X2+V0=
```

now you need to the public key from the server:
```
$ cat server.publickey
7lTo3CyQ/5SJgxGgtHyWVwgAKmbIuzQhPt4L6z1ZqlY=
```

> **Please Note:** These keys are for demonstration purposes only. Please do not use in your actual config files.

`/etc/wireguard/wg0.conf` on Controller device:
```
[Interface]
PrivateKey = <Controller Private Key>
ListenPort = 21841
Address = 192.168.3.2/24

[Peer]
PublicKey = <Server Public Key>
Endpoint = <Server Public IP Address>:51820
## Using 0.0.0.0/0 will send ALL traffic through the VPN 
## where as using 192.168.3.0/24 will send only traffic 
# AllowedIPs = 0.0.0.0/0
AllowedIPs = 192.168.3.0/24
```

`/etc/wireguard/wg0.conf` on buggy device
```
[Interface]
PrivateKey = <Buddy Private Key>
ListenPort = 21841
Address = 192.168.3.3/24

[Peer]
PublicKey = <Server Public Key>
Endpoint = <Server Public IP Address>:51820
## Using 0.0.0.0/0 will send ALL traffic through the VPN 
## where as using 192.168.3.0/24 will send only traffic 
# AllowedIPs = 0.0.0.0/0
AllowedIPs = 192.168.3.0/24
```

## Step 6: Start WireGuard

Once you have WireGuard setup you need so start the server service. You do this by running the following command on each device:
```
sudo wg-quick up wg0
```

If everything has been configured correctly you should be able to ping each device on the network:
```
ping 192.168.3.1
ping 192.168.3.2
ping 192.168.3.3
``` 

## Step 7: Modify Our Code

Using the code from `projects\remote-controller\robby-remote.py` modify the host with the new IP address.

```python
# To address this bug we set the global pin factory to the remote host
# and connect to the breadboard controller through a localhost pin_factory.
Device.pin_factory = PiGPIOFactory(host='192.168.3.3')
robot = Robot(left=(7,8), right=(9,10))
```

You should now be able to control your Pi over the VPN network.
