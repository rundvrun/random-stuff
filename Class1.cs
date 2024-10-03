using System;
using OpenQA.Selenium.Appium.Enums;
using OpenQA.Selenium.Appium.Android;
using OpenQA.Selenium.Remote;
using NUnit.Framework;

namespace SeleniumTest
{
    public static class Env
    {
        public static String rootDirectory = System.IO.Path.GetFullPath($"{System.AppDomain.CurrentDomain.BaseDirectory.ToString()}/../../../..");

        static public bool IsSauce()
        {
            return Environment.GetEnvironmentVariable("SAUCE_LABS") != null;
        }

        static public Uri ServerUri()
        {
            String sauceUserName = Environment.GetEnvironmentVariable("SAUCE_USERNAME");
            String sauceAccessKey = Environment.GetEnvironmentVariable("SAUCE_ACCESS_KEY");

            return (sauceUserName == null) || (sauceAccessKey == null)
                ? new Uri("http://localhost:4723/wd/hub")
                : new Uri($"https://{sauceUserName}:{sauceAccessKey}@ondemand.saucelabs.com:80/wd/hub");
        }

        public static TimeSpan INIT_TIMEOUT_SEC = TimeSpan.FromSeconds(180);
        public static TimeSpan IMPLICIT_TIMEOUT_SEC = TimeSpan.FromSeconds(10);
    }
    [TestFixture()]
    public class Class1
    {
        static AndroidDriver<AndroidElement> driver;
        [SetUp()]
        public static void SetUp()
        {
            DesiredCapabilities capabilities = new DesiredCapabilities();
            capabilities.SetCapability(MobileCapabilityType.BrowserName, "");
            capabilities.SetCapability(MobileCapabilityType.PlatformName, "Android");
            capabilities.SetCapability(MobileCapabilityType.PlatformVersion, "5.1");
            capabilities.SetCapability(MobileCapabilityType.AutomationName, "UIAutomator2");
            capabilities.SetCapability(MobileCapabilityType.DeviceName, "Galaxy J1");
            //capabilities.SetCapability("appActivity", ".app.SearchInvoke");
            capabilities.SetCapability(MobileCapabilityType.App, "F:\\ApiDemos-debug.apk");

            driver = new AndroidDriver<AndroidElement>(Env.ServerUri(), capabilities, Env.INIT_TIMEOUT_SEC);
            driver.Manage().Timeouts().ImplicitlyWait(Env.IMPLICIT_TIMEOUT_SEC);
        }
        [TearDown()]
        public static void TearDown()
        {
            driver.Quit();
        }

        public static AndroidElement ScrollToElement(string elementText)
        {
            return driver.FindElementByAndroidUIAutomator($"new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().textMatches(\"{elementText}\").instance(0))");
        }

        [Test]
        public void TestLogTextBoxAdd()
        {
            ScrollToElement("Text").Click();
            driver.FindElementByAccessibilityId("LogTextBox").Click();
            driver.FindElementByAccessibilityId("Add").Click();
            var txtBox = driver.FindElementById("io.appium.android.apis:id/text");
            Assert.IsNotEmpty(txtBox.Text);
            var old = txtBox.Text;
            driver.FindElementByAccessibilityId("Do nothing").Click();
            Assert.AreEqual(old, driver.FindElementById("io.appium.android.apis:id/text").Text);
        }
        [Test]
        public void TestViewFlip()
        {
            driver.FindElementByAccessibilityId("Animation").Click();
            ScrollToElement("View Flip").Click();
            var elemXpath = "/hierarchy/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.TextView[1]";
            Assert.AreEqual("One", driver.FindElementByXPath(elemXpath).Text);
            driver.FindElementByAccessibilityId("Flip").Click();
            Assert.AreEqual("Un", driver.FindElementByXPath(elemXpath).Text);
            driver.FindElementByAccessibilityId("Flip").Click();
            Assert.AreEqual("One", driver.FindElementByXPath(elemXpath).Text);
        }
        [Test]
        public void TestCustomTitle()
        {
            driver.FindElementByAccessibilityId("App").Click();
            driver.FindElementByAccessibilityId("Activity").Click();
            driver.FindElementByAccessibilityId("Custom Title").Click();

            var leftTxtBox = driver.FindElementById("io.appium.android.apis:id/left_text_edit");
            var leftTxtBtn = driver.FindElementById("io.appium.android.apis:id/left_text_button");
            leftTxtBox.Clear();
            leftTxtBox.SendKeys("Hello");
            leftTxtBtn.Click();
            var leftTxt = driver.FindElementById("io.appium.android.apis:id/left_text");
            Assert.AreEqual("Hello", leftTxt.Text);

            var rightTxtBox = driver.FindElementById("io.appium.android.apis:id/right_text_edit");
            var rightTxtBtn = driver.FindElementById("io.appium.android.apis:id/right_text_button");
            rightTxtBox.Clear();
            rightTxtBox.SendKeys("World");
            rightTxtBtn.Click();
            var rightTxt = driver.FindElementById("io.appium.android.apis:id/right_text");
            Assert.AreEqual("World", rightTxt.Text);
        }
    }
}
