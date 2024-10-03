using OpenQA.Selenium.Firefox;
using OpenQA.Selenium;
using NUnit.Framework;

namespace TestSeleniumDriver
{
    class TestSelenium
    {
        [Test]
        public static void TC01()
        {
            var driver = new FirefoxDriver();
            string baseUrl = "https://demo.opencart.com/";
            driver.Navigate().GoToUrl(baseUrl);
            var btn43 = driver.FindElement(By.XPath("//button[contains(@onclick, '43')]"));
            Assert.AreEqual("cart.add('43');", btn43.GetAttribute("onclick"));
            btn43.Click();
        }
    }
}
