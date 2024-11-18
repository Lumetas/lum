package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
)

const BIN_DIR = "C:\\Users\\User.DESKTOP-24K78MD\\bin"
const SHELL = "powershell"

func run_command(command string, args ...string) (string, error) {
	// Создаем команду
	cmd := exec.Command(command, args...)

	// Создаем буфер для захвата стандартного вывода
	var output bytes.Buffer
	cmd.Stdout = &output
	cmd.Stderr = &output // Захватываем стандартный вывод ошибок тоже

	// Выполняем команду
	err := cmd.Run()
	if err != nil {
		return "", fmt.Errorf("ошибка выполнения команды: %v: %s", err, output.String())
	}

	return output.String(), nil
}

func remove_file(filepath string) error {
	err := os.Remove(filepath)
	if err != nil {
		return fmt.Errorf("ошибка при удалении файла %s: %v", filepath, err)
	}
	return nil
}

func download_file(url string, filename string) error {
	// Проверяем и создаем директорию, если она не существует
	if err := os.MkdirAll(BIN_DIR, os.ModePerm); err != nil {
		return fmt.Errorf("не удалось создать директорию: %v", err)
	}

	// Создаем новый HTTP-запрос
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Проверяем код ответа
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("ошибка HTTP: статус код %d", resp.StatusCode)
	}

	// Создаем файл в указанной папке
	filePath := filepath.Join(BIN_DIR, filename)
	out, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer out.Close()

	// Получаем общий размер файла
	totalSize := resp.ContentLength
	// fmt.Println(totalSize)
	var downloaded int64

	// Создаем буфер для записи
	buffer := make([]byte, 1024) // 1 КБ
	for {
		// Читаем данные из ответа
		n, err := resp.Body.Read(buffer)
		if n > 0 {
			// Записываем данные в файл
			out.Write(buffer[:n])
			downloaded += int64(n)

			// Обновляем прогресс-бар
			printProgress(downloaded, totalSize)
		}
		if err == io.EOF {
			break // Конец файла
		}
		if err != nil {
			return err
		}
	}

	// fmt.Printf("\nСкачано %d байт\n", downloaded)
	return nil
}

// printProgress выводит прогресс-бар в консоль
// printProgress выводит прогресс-бар в консоль
func printProgress(downloaded, total int64) {
	if total == 0 {
		return // Если total равен 0, ничего не делаем
	}

	percent := float64(downloaded) / float64(total) * 100
	barLength := 50 // Длина прогресс-бара
	done := int(percent / (100 / float64(barLength)))

	// Ограничиваем значение done в корректных пределах
	if done > barLength {
		done = barLength
	} else if done < 0 {
		done = 0
	}

	// Форматируем строку прогресс-бара
	progressBar := fmt.Sprintf("\r%.2f%% ", percent)

	// Убираем первую часть строки и добавляем пробелы для визуального отображения
	fmt.Print(progressBar)
}

func read_config(str string) []string {
	return strings.Split(str, "\n")
}

func send_get_req(url string) string {
	// Создаем HTTP-клиент с заголовком User-Agent
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		// fmt.Printf("Ошибка при создании запроса: %v\n", err)
		return ""
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

	// Выполняем запрос
	resp, err := client.Do(req)
	if err != nil {
		// fmt.Printf("Ошибка при выполнении запроса: %v\n", err)
		return ""
	}
	defer resp.Body.Close()

	// Проверяем статус ответа
	if resp.StatusCode != http.StatusOK {
		// fmt.Printf("Ошибка ответ сервера: %s\n", resp.Status)
		return ""
	}

	// Читаем тело ответа
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		// fmt.Printf("Ошибка при чтении ответа: %v\n", err)
		return ""
	}

	// Преобразуем ответ в строку
	bodyStr := string(body)
	return bodyStr
}

func get_repo_config(url string) string {
	parts := strings.Split(url, "/")
	user := parts[3]
	repo := parts[4]
	url = "https://raw.githubusercontent.com/" + user + "/" + repo + "/refs/heads/main/lum.conf"
	result := send_get_req(url)
	return result
	return ""
}

func isUserInURL(url string, author string) bool {
	// Разделяем URL по слешам
	parts := strings.Split(url, "/")

	// Проверяем, что URL имеет правильный формат
	if len(parts) >= 5 { // ожидаем, что URL будет в формате https://github.com/<user>/<repo>
		user := parts[3] // <user> находится на 5-й позиции
		return user == author
	}

	// return false // Если формат URL неверный, возвращаем false
	return true
}

func searchGitHub(packageName string) string {
	searchURL := fmt.Sprintf("https://github.com/search?q=lumpackage%%3D%s%%20in%%3Adescription", packageName)
	bodyStr := send_get_req(searchURL)
	// Регулярное выражение для поиска ссылок в div c классом search-title
	re := regexp.MustCompile(`<div[^>]*class="[^"]*search-title[^"]*"[^>]*>.*?<a[^>]*href="(/[^"]+)"`)
	matches := re.FindAllStringSubmatch(bodyStr, -1)

	// Печатаем подходящие ссылки
	if len(matches) > 0 {
		for _, match := range matches {
			if len(match) > 1 {
				repoLink := "https://github.com" + match[1]
				if len(os.Args) > 3 {
					if isUserInURL(repoLink, os.Args[3]) {
						return repoLink
					}
				} else {
					return repoLink
				}
			}
		}
	} else {
		// Если ссылки не найдены
		// fmt.Println("Репозитории не найдены.")
	}
	return ""
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("usage: go run search_github.go <command> <package_name> (author)")
		os.Exit(1)
	}

	if os.Args[1] == "install" {

		url := searchGitHub(os.Args[2])
		if url != "" {
			config := read_config(get_repo_config(url))
			you_want_string := ""
			if config[0] == "source" {
				you_want_string = "Do you want to install source package " + url + "? In the process, he will execute his commands" + " y/n "
			} else {
				you_want_string = "Do you want to install " + url + "?" + " y/n "
			}
			fmt.Println(you_want_string)
			var userInput string

			// Запрашиваем ввод у пользователя
			_, err := fmt.Scanln(&userInput)
			if err != nil {
				fmt.Println("Error", err)
				return
			}

			if userInput == "y" {
				if config[0] == "bin" {
					download_file(config[1], strings.Split(url, "/")[4])

				} else if config[0] == "source" {
					str, err := run_command(SHELL, "-c", "cd ~ ; git clone "+url+" ; cd "+strings.Split(url, "/")[4]+" ; "+config[1])
					if err == nil {
						fmt.Println(str)
					}
				}
				fmt.Println("Done")
			} else {
				fmt.Println("Cancelled")
			}
		} else {
			fmt.Println("Sorry, package not found")
		}

	} else if os.Args[1] == "remove" {
		url := searchGitHub(os.Args[2])
		if url != "" {
			config := read_config(get_repo_config(url))
			you_want_string := ""
			if config[0] == "source" {
				you_want_string = "Do you want to remove source package " + url + "? In the process, he will execute his commands" + " y/n "
			} else {
				you_want_string = "Do you want to remove " + url + "?" + " y/n "
			}
			// you_want_string := "Do you want to remove " + url + "?" + " y/n "
			fmt.Println(you_want_string)
			var userInput string

			// Запрашиваем ввод у пользователя
			_, err := fmt.Scanln(&userInput)
			if err != nil {
				fmt.Println("Error", err)
				return
			}

			if userInput == "y" {
				if config[0] == "bin" {
					name := strings.Split(url, "/")[4]
					remove_file(filepath.Join(BIN_DIR, name))

				} else if config[0] == "source" {
					str, err := run_command(SHELL, "-c", "cd ~ ; git clone "+url+" ; cd "+strings.Split(url, "/")[4]+" ; "+config[2])
					if err == nil {
						fmt.Println(str)
					}
				}

				fmt.Println("Done")
			} else {
				fmt.Println("Cancelled")
			}

		}
	}
}
