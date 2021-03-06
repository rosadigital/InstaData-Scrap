# InstaData-Scrap
## 💻 About this project (sobre este projeto)
:us: This project aimed to scrap on a given public Instagram profile some of the main information available about posts and followers.

:brazil: Este projeto teve por objetivo obter, em um dado perfil público do Instagram, algumas das principais informações disponíveis sobre posts e seguidores.

---
## ⚙️ Project demonstration (demontração do projeto)
The algorithm generates 03 Reports:
- Report 01, which contains:
  - post_link;
  - post_date;
  - amount_of_likes;
  - post_link_type (img or vid).
<p align="center"> <img alt="example_report_01.JPG" title="example_report_01.JPG" src="./assets/example_report_01.jpg" width="800px">

- Report 02, derived from Report 01, which contains:
  - post_link_type (img or vid);
  - post_link;
  - post_date;
  - amount_of_likes;
  - likers_links; and
  - likers_names.
<p align="center"> <img alt="example_report_02.JPG" title="example_report_02.JPG" src="./assets/example_report_02.jpg" width="1000px">
   
- Report 03, derived from Report 01, which contains:
  - followers_links,
  - followers_names;
  - followers_amount_of_posts;
  - followers_amount_of_followers;
  - followers_amount_of_following;
  - followers_private_or_public_profile_status; and
  - followers_bio_description.
<p align="center"> <img alt="example_report_03.JPG" title="example_report_03.JPG" src="./assets/example_report_03.jpg" width="2000px">

The example of data scraped can be seen here:
- [report01_sample.csv](./report_samples/report_01_coisandoporai.csv)
- [report02_sample.csv](./report_samples/report_02_coisandoporai.csv)
- [report03_sample.csv](./report_samples/report_03_coisandoporai.csv)

---
	
## 💡 Knowledge acquired (conhecimentos adquiridos)

- During this project, I learned:
  - use **object-oriented programming (OOP)** to create reusable codes for future programming;
  - scrap website information using BeautifulSoup and Selenium; and
  - organize scrapped data and use it for future scrapping process.

---

## 🚀 How to execute this project (como executar este projeto)

 - To run the code it is recommended to use an IDE, such as Pycharm;
  - Just clone this project, open on your IDE, and run the file main.py
  - From main.py, this file will run:
    - DB01: for a draft of report 01;
    - DB02: for the report 02 and a final report 01; and
    - DB03: for the report 03.
  - Note: by commenting DB01 or DB02 or DB03, on main.py, it is possible to do not generate, respectively, the reports 01, 02, and 03. 

### 🎲 Requirements (requisitos)

To run the code, it is recommended to install the following Python Packaged:
- beautifulsoup4==4.9.3
- bs4==0.0.1
- certifi==2020.12.5
- chardet==4.0.0
- idna==2.10
- numpy==1.20.2
- pandas==1.2.4
- python-dateutil==2.8.1
- pytz==2021.1
- requests==2.25.1
- selenium==3.141.0
- six==1.15.0
- soupsieve==2.2.1
- urllib3==1.26.4



#### Running the codes (rodando os códigos)

```bash

# Clone this repository
$ git@github.com:rosadigital/InstaData-Scrap.git
# Open the repository on pycharm

```

---

## 🦸 Author (autor)


Felipe Rosa on [LinkedIn](https://www.linkedin.com/in/felipe-rosa/)

---

## 📝 License (licença)

This project is licensed under [MIT](./LICENSE).

Este projeto esta sobe a licença [MIT](./LICENSE).

Made with ❤️ by Felipe Rosa 👋🏽 [Contact here!](https://www.linkedin.com/in/felipe-rosa/)

Feito com ❤️ por Felipe Rosa 👋🏽 [Entre em contato!](https://www.linkedin.com/in/felipe-rosa/)

--
