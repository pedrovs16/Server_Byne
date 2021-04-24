import PySimpleGUI as sg
import main_cliente_copia

class TelaPython:
    def __init__(self):
        # SISTEMA INTEIRO
            # LAYOUT
            inicio = [
                [sg.Text('=' * 120)],
                [sg.Text('CLIENT'.center(113))],
                [sg.Text('=' * 120)],
                # 1° LINHA
                [sg.Text('Server IP', size=(7, 0)), sg.Input(size=(20,0), key= 'join_server'), sg.Button('Join server')],
                # OUTPUT
                [sg.Text('=' * 120)],
                [sg.Output(size=(65, 15))],
                [sg.Text('=' * 120)],
                # 2° LINHA
                [sg.Text('Decide between odd, even or disconnect[O/E/!DISCONNECT] ')],
                [sg.Text('Decision', size=(7, 0)), sg.Input(size=(20, 0), key='decision'), sg.Button('Make decision')],
            ]
            # JANELA
            janela = sg.Window('Caixa', size=(500, 500)).layout(inicio)
            # INFOS ARQUIVO COM OS DADOS

            # TROCA DE INFOS ENTRE O COMPUTADOR E O USUÁRIO
            while True:
                event, values = janela.read()
                if event == sg.WINDOW_CLOSED:
                    break
                elif event == 'join_server':
                    pass
                elif event == 'decision':
                    pass

tela = TelaPython()
