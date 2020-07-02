import Channel

class bot:
    pass

if __name__ == '__main__':
    cn = Channel.Channel('ENDERZOMBI102')
    while True:
        try:
            print( eval( input('The_end3rbot>') ) )
        except Exception as e:
            if e is not None:
                print(e)