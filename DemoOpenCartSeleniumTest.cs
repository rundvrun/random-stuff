using System;
using System.Text.RegularExpressions;
using System.Threading;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Support.UI;

namespace SeleniumTest
{
    [TestClass]
    public class DemoOpenCartSeleniumTest
    {
        FirefoxDriver driver;
        [TestInitialize]
        public void SetUp()
        {
            driver = new FirefoxDriver();
            var baseUrl = "https://demo.opencart.com/";
            driver.Navigate().GoToUrl(baseUrl);
        }
        [TestCleanup]
        public void TearDown()
        {
            driver.Close();
        }

        [TestMethod, Description("Input: Page, Output: Init cart total = $0.00"), Timeout(20000)]
        public void TC_EmptyCart_Message()
        {
            var element = driver.FindElementByCssSelector("#cart-total");
            Assert.IsNotNull(element);
            Assert.AreEqual("0 item(s) - $0.00", element.Text);
        }
        [TestMethod, Description("Input: Phones & PDAs, Output: 3"), Timeout(20000)]
        public void TC_Number_Of_Product()
        {
            driver.FindElementByXPath("//a[text() = 'Phones & PDAs']").Click();
            Thread.Sleep(1200);
            var text = driver.FindElementByCssSelector(".list-group-item.active").Text;
            var products = driver.FindElementsByClassName("product-thumb");
            var product_cate = driver.FindElementByCssSelector("#content>h2").Text;
            Assert.AreEqual($"{product_cate} ({products.Count})", text);
        }
        [TestMethod, Description("Input: Add 1 item (43), Output: 1 item(s) in cart ($602.00)"), Timeout(20000)]
        public void TC_Add_1_Item()
        {
            var button = driver.FindElementByCssSelector("button[onclick=\"cart.add('43');\"]");
            Assert.IsNotNull(button);
            button.Click();
            Thread.Sleep(1000);
            var element = driver.FindElementByCssSelector("#cart-total");
            Assert.IsNotNull(element);
            Assert.AreEqual("1 item(s) - $602.00", element.Text);
        }
        [TestMethod, Description("Input: 1-item cart, Output: Empty cart"), Timeout(20000)]
        public void TC_Remove_1_Item()
        {
            var button = driver.FindElementByCssSelector("button[onclick=\"cart.add('43');\"]");
            Assert.IsNotNull(button);
            button.Click();
            Thread.Sleep(1000);
            var cart_button = driver.FindElementByCssSelector("#cart>button");
            cart_button.Click();
            Thread.Sleep(1000);
            var remove_button = driver.FindElementByCssSelector("button[title='Remove']");
            Assert.IsNotNull(remove_button);
            remove_button.Click();
            Thread.Sleep(1500);
            cart_button.Click();
            Thread.Sleep(1000);
            var text = driver.FindElementByCssSelector("#cart>ul>li>p").Text;
            Assert.AreEqual("Your shopping cart is empty!", text);
        }
        [TestMethod, Description("Input: Empty Category (Software), Output: There are no products to list in this category."), Timeout(20000)]
        public void TC_Category_0_Item()
        {
            driver.FindElementByXPath("//a[text() = 'Software']").Click();
            Thread.Sleep(1200);
            var text = driver.FindElementByCssSelector(".list-group-item.active").Text;
            Assert.IsTrue(text.Contains("(0)"));
            var message = driver.FindElementByCssSelector("#content>p").Text;
            Assert.AreEqual("There are no products to list in this category.", message);
        }
        [TestMethod, Description("Input: Phones & PDAs, Output: Sort Descending By Price"), Timeout(20000)]
        public void TC_Desc_Price()
        {
            driver.FindElementByXPath("//a[text() = 'Phones & PDAs']").Click();
            Thread.Sleep(1200);
            new SelectElement(driver.FindElementById("input-sort")).SelectByText("Price (High > Low)");
            var items = driver.FindElementsByClassName("price");
            bool desc = true;
            double curr_price = Double.MaxValue - 1;
            var regex = new Regex(@"\$(\d+\.\d+)*");
            foreach (var item in items)
            {
                double price = Convert.ToDouble(regex.Match(item.Text).Groups[1].Value);
                if (price > curr_price)
                {
                    desc = false;
                    break;
                }
                curr_price = price;
            }
            Assert.IsTrue(desc);
        }
        [TestMethod, Description("Input: Phones & PDAs, Output: Sort Ascending By Name"), Timeout(20000)]
        public void TC_Asc_Name()
        {
            driver.FindElementByXPath("//a[text() = 'Phones & PDAs']").Click();
            Thread.Sleep(1200);
            new SelectElement(driver.FindElementById("input-sort")).SelectByText("Name (A - Z)");
            var items = driver.FindElementsByCssSelector(".caption>h4>a");
            bool asc = true;
            for (int i = 1; asc && i < items.Count; ++i) 
                asc = String.Compare(items[i - 1].Text, items[i].Text) <= 0;
            Assert.IsTrue(asc);
        }
        [TestMethod, Description("Input: 19-item page, Output: There are no more 25 items in page"), Timeout(20000)]
        public void TC_List_Limit_25()
        {
            driver.FindElementByName("search").SendKeys(" ");
            driver.FindElementByCssSelector(".input-group-btn > button").Click();
            new SelectElement(driver.FindElementById("input-limit")).SelectByText("25");
            Assert.IsTrue(25 >= driver.FindElementsByClassName("product-thumb").Count);
        }
        [TestMethod, Description("Input: 19-item page, Output: 15-item page (limit)"), Timeout(20000)]
        public void TC_List_Limit_15()
        {
            driver.FindElementByName("search").SendKeys(" ");
            driver.FindElementByCssSelector(".input-group-btn > button").Click();
            new SelectElement(driver.FindElementById("input-limit")).SelectByText("15");
            Assert.AreEqual(15, driver.FindElementsByClassName("product-thumb").Count);
        }
        [TestMethod, Description("Input: Change currency to EUR, Output: Currency is €"), Timeout(20000)]
        public void TC_Change_Currency_To_EUR()
        {
            driver.FindElementByCssSelector("#form-currency > .btn-group > button").Click();
            driver.FindElementByName("EUR").Click();
            driver.FindElementByName("search").SendKeys(" ");
            driver.FindElementByCssSelector(".input-group-btn > button").Click();
            new SelectElement(driver.FindElementById("input-limit")).SelectByText("50");
            bool isChanged = true;
            foreach (var item in driver.FindElementsByClassName("price"))
            {
                if (!item.Text.Contains("€"))
                {
                    isChanged = false;
                    break;
                }
            }
            Assert.IsTrue(isChanged);
        }
    }
}
