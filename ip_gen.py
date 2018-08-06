ip_file = open('ip_file.txt')

for ip_line in ip_file.readlines():

    # treatment ip file
    ip_line = ip_line.strip('\n')
    ip_list = ip_line.split('.')
    mask_list = ip_list[3].split('/')

    # treatment ip for a.b.c.d/mask
    mask = int(mask_list[1])
    ip_a = ip_list[0]
    ip_b = ip_list[1]
    ip_c = ip_list[2]
    ip_d = mask_list[0]
    ip_first = str (ip_a) + '.' + str (ip_b) + '.' + str (ip_c) + '.' + str (ip_d)
    print(ip_first)
    # Number of hosts by mask
    mask_32 = 32

    if mask != 32:
        number_hosts = int(2**(mask_32-mask))
    else:
        number_hosts = 1
    print(number_hosts)

    # write all ip in hosts file

    baba = 0
    hosts_file = open ('hosts_file.txt', 'w')
    hosts_file.write (ip_first + '\n')
    number_hosts -= 1

    while baba == 0:

        if number_hosts >= 1:
            summ = int(ip_a) * 256 ** 3 + int(ip_b) * 256 ** 2 + int(ip_c) * 256 + int(ip_d) + 1
            ip_d = summ % 256
            ip_c = (summ // (256 ** 1)) % 256
            ip_b = (summ // (256 ** 2)) % 256
            ip_a = (summ // (256 ** 3)) % 256

            if ip_d != 255 and ip_d != 0:
                ip = str(ip_a) + '.' + str(ip_b) + '.' + str(ip_c) + '.' + str(ip_d)
                hosts_file.write(ip + '\n')
                number_hosts -= 1
            else:
                number_hosts -= 1
        else:
            baba = 1


ip_file.close()
