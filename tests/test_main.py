"""Pruebas de main.py: que arranque con los datos de ejemplo y no truene con
Ctrl+C / Ctrl+D ni con opciones invalidas en el menu principal. (T23, T24)"""

import main


def entradas(valores):
    respuestas = iter(valores)
    return lambda _mensaje="": next(respuestas)


def test_opcion_invalida_en_menu_principal_no_truena(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", entradas(["x", "99", "5"]))

    main.main()

    salida = capsys.readouterr().out
    assert "Opción no válida" in salida
    assert "Hasta luego" in salida


def test_ctrl_c_en_menu_principal_sale_con_mensaje(monkeypatch, capsys):
    def input_con_ctrl_c(_mensaje=""):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", input_con_ctrl_c)

    main.main()  # no debe lanzar KeyboardInterrupt hacia afuera

    assert "Hasta luego" in capsys.readouterr().out


def test_ctrl_c_dentro_de_un_submenu_sale_con_mensaje(monkeypatch, capsys):
    # Entra a Materiales y ahí "presiona" Ctrl+C a medio registro de un libro
    respuestas = iter(["1", "1"])

    def input_falso(_mensaje=""):
        try:
            return next(respuestas)
        except StopIteration:
            raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", input_falso)

    main.main()

    assert "Hasta luego" in capsys.readouterr().out


def test_eof_en_menu_principal_sale_con_mensaje(monkeypatch, capsys):
    def input_con_eof(_mensaje=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", input_con_eof)

    main.main()

    assert "Hasta luego" in capsys.readouterr().out
