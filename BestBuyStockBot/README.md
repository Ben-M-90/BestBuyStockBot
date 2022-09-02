<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center"><a href="https://github.com/ben-m-90/bestbuystockbot">BestBuyStockBot</a></h3>

  <p align="center">
    Bot for monitoring GPU stock availability at Best Buy and purchasing once stock has returned. Can also be used for other Best Buy products with a desired product URL.
    <br />
    <a href="https://github.com/ben-m-90/bestbuystockbot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ben-m-90/bestbuystockbot/issues">Report Bug</a>
    ·
    <a href="https://github.com/ben-m-90/bestbuystockbot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/ben-m-90/bestbuystockbot)

Developed during the Great GPU Shortage of 2021. Bot uses Selenium to control a Chrome web driver with a custom user agent and various other strategies to mask bot presence. Utilizes some shortcuts to speed up purchasing process.
Status updates pushed to configurable Discord channel via Discord webhook so current status can be monitored remotely.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![Selenium][Selenium.dev]][Selenium-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Before beginning setup, it is recommended to [https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments](create and activate a Python virtual environment).

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/ben-m-90/bestbuystockbot.git
    ```
2. Navigate your terminal to the local storage location created in Step 1.
2. Install packages from requirements.txt
    ```sh
    pip install -r requirements.txt
    ```
3. Rename 'sample.env' to '.env'
4. Edit '.env' in a text editor.
* DISCORD_TOKEN, DISCORD_GUILD, MENTION_ID, and WEBHOOK_URL will be set by Discord. See [https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks](Discord documentation on creating webhooks).
* LOGIN_EMAIL, LOGIN_PASSWORD, and CVV are your login information for BestBuy.com. Default payment methods and shipping addresses must be setup through BestBuy.com. CVV will be your credit card CVV used for finalizing a purchase. The bot will use your default payment method associated with your BestBuy.com account. No payment information is passed through or stored by this bot, only CVV.
* Add URLs for products to be monitor, separated by commas and on new lines.
    ```
    DISCORD_TOKEN = ""
    DISCORD_GUILD = "" 
    MENTION_ID = ""
    WEBHOOK_URL = ""

    LOGIN_EMAIL = ""
    LOGIN_PASSWORD = ""
    CVV = ""

    URL_LIST = "
    https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440,
    https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400,
    https://www.bestbuy.com/site/asus-rog-strix-g15-advantage-edition-15-6-fhd-gaming-laptop-amd-ryzen-9-5900hx-16gb-memory-radeonrx-6800m-512gb-ssd/6466550.p?skuId=6466550"
    ```
5. Additional settings are available in stock_bot.py
* Set 'PRINT_TO_DISCORD' to True to enable printing status updates to the Discord webhook configured in Step 4.
6. Run bot in your Python Virtual Environment. Note that the shortcut py may not work on all systems and is dependent on how your local Python installation is configured. 
    ```sh
    py stock_bot.py
    ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After properly configuring, the bot will cycle through list of provided URLs and check if stock is available. It will continue to do this until it detects a product has return to stock.
Once a product has been detected as in stock the bot will execute a purchase process where the product will be purchased. Default payment methods and shipping locations must be setup through BestBuy.com for this to work.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Extend functionality to work with other websites outside of BestBuy (e.g. Amazon, Newegg)

See the [open issues](https://github.com/ben-m-90/bestbuystockbot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/ben-m-90/bestbuystockbot](https://github.com/ben-m-90/bestbuystockbot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ben-m-90/bestbuystockbot.svg?style=for-the-badge
[contributors-url]: https://github.com/ben-m-90/bestbuystockbot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ben-m-90/bestbuystockbot.svg?style=for-the-badge
[forks-url]: https://github.com/ben-m-90/bestbuystockbot/network/members
[stars-shield]: https://img.shields.io/github/stars/ben-m-90/bestbuystockbot.svg?style=for-the-badge
[stars-url]: https://github.com/ben-m-90/bestbuystockbot/stargazers
[issues-shield]: https://img.shields.io/github/issues/ben-m-90/bestbuystockbot.svg?style=for-the-badge
[issues-url]: https://github.com/ben-m-90/bestbuystockbot/issues
[license-shield]: https://img.shields.io/github/license/ben-m-90/bestbuystockbot.svg?style=for-the-badge
[license-url]: https://github.com/ben-m-90/bestbuystockbot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ben-a-miller
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Python.org]: https://img.shields.io/badge/Python-#3776AB?style=for-the-badge&logo=Python&logoColor=white
[Python-url]: https://python.org 
[Selenium.dev]: https://img.shields.io/badge/Selenium-##43B02A?style=for-the-badge&logo=Selenium&logoColor=white
[Selenium-url]: https://selenium.dev