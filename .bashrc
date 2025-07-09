export PATH="$PATH:$HOME/cage_lang"

function cage {
    if [ $# -eq 0 ]; then
        echo "Использование: cage имя_файла.cg"
        return 1
    elif [ $# -eq 1 ]; then
        if [[ "$1" == *.cg ]]; then
            if [ "$1" == ".cg" ]; then
                echo "Ошибка: укажите имя файла перед расширением .cg"
                return 1
            else
                python ~/cage_lang/cg_interpreter.pyc "$@"
            fi
        else
            echo "Ошибка: укажите расширение .cg в конце имени файла"
            return 1
        fi
    else
        python ~/cage_lang/cg_interpreter.pyc "$@"
    fi
}

cp0() {
    if [ $# -eq 0 ]; then
        echo "Ошибка: укажите файлы для копирования"
        return 1
    fi
    cp "$@" "/storage/emulated/0/"
}

mv0() { mv "$1" "/storage/emulated/0"; }

cd0() {
    local target="/storage/emulated/0"
    if [ $# -gt 0 ]; then
        target="$target/$1"
    fi
    cd "$target"
}

function pkg() {
    case "$1" in
        "install")
            case "$2" in
                "cage")
                    echo "[*] Установка CageLang из GitHub..."
                    if [ -d ~/cage_lang ]; then
                        echo "[!] Папка ~/cage_lang уже существует. Используйте 'pkg update cage' для обновления."
                    else
                        git clone https://github.com/arseniy-cage/cagelang.git ~/cage_lang
                        if [ -d ~/cage_lang/CageLang ]; then
                            mv ~/cage_lang/CageLang/* ~/cage_lang/
                            rm -rf ~/cage_lang/CageLang
                        fi
                        echo "[+] CageLang успешно установлен в ~/cage_lang!"
                        cd ~
                    fi
                    ;;
                *)
                    command pkg "$@"
                    ;;
            esac
            ;;
        "update")
            case "$2" in
                "cage")
                    echo "[*] Обновление CageLang..."
                    if [ -d ~/cage_lang ]; then
                        rm -rf ~/cage_lang
                        git clone https://github.com/arseniy-cage/cagelang.git ~/cage_lang
                        if [ -d ~/cage_lang/CageLang ]; then
                            mv ~/cage_lang/CageLang/* ~/cage_lang/
                            rm -rf ~/cage_lang/CageLang
                        fi
                        echo "[+] CageLang успешно обновлён!"
                        cd ~
                    else
                        echo "[!] Папка ~/cage_lang не найдена. Сначала выполните 'pkg install cage'."
                    fi
                    ;;
                *)
                    command pkg "$@"
                    ;;
            esac
            ;;
        "uninstall")
            case "$2" in
                "cage")
                    echo "[*] Удаление CageLang..."
                    if [ -d ~/cage_lang ]; then
                        read -p "Вы уверены, что хотите удалить CageLang? [Y/n] " confirm
                        case $confirm in
                            [yY]|[yY][eE][sS]|"")
                                echo "Удаление ~/cage_lang..."
                                rm -rf ~/cage_lang
                                echo "[+] CageLang успешно удалён!"
                                ;;
                            *)
                                echo "[!] Удаление отменено"
                                ;;
                        esac
                    else
                        echo "[!] Папка ~/cage_lang не найдена. CageLang не установлен."
                    fi
                    ;;
                *)
                    command pkg "$@"
                    ;;
            esac
            ;;
        *)
            command pkg "$@"
            ;;
    esac
}
