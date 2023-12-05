import os


class Firewall:

    def ban(self, address):
        pass

    def unban(self, address):
        pass

    def isBanned(self, address):
        pass


class UFW(Firewall):

    def ban(self, address):
        os.system(f'ufw insert 1 deny from {address}')
        os.system(f'conntrack -D -s {address}')
        # TODO: completely drop the existing connection

    def unban(self, address):
        os.system(f'ufw delete deny from {address}')

    def isBanned(self, address):
        # temporary use storage.isBanned instead of this function
        # TODO: add grep
        pop = os.popen(f'ufw status').read()
        return False

# TODO: add Fail2ban, IPTables