def logging(log, log_file):
    file = open(log_file, 'a')
    print(log)
    file.write(f'{log}\n')
    file.close()

