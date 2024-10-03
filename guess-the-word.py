import clr
import random
import glob
import win32com.client 

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference("System")

from System import Environment
from System.Windows.Forms import Application, Form, TextBox, ImageLayout, Timer, MessageBox, Label, DockStyle
from System.Drawing import Size, Font, Image

images = random.sample((l := glob.glob('*.jpg')), k=min(len(l), 35))

class MainForm(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = "Type what you see to unlock"
        self.Width = 1700
        self.Height = 1000
        self.BackgroundImageLayout = ImageLayout.Stretch
        self.ControlBox = False
        self.speechSynthesizer = win32com.client.Dispatch("SAPI.SpVoice") 

        self.textBox1 = TextBox()
        self.textBox1.Font = Font(self.textBox1.Font.FontFamily, 50)
        self.textBox1.Size = Size(1600, 990)
        self.textBox1.KeyPress += self.Text_Changed
        self.textBox1.Dock = DockStyle.Top

        self.label1 = Label()
        self.label1.Dock = DockStyle.Bottom

        self.Controls.Add(self.textBox1)
        self.Controls.Add(self.label1)

        self.timer = Timer()
        self.timer.Interval = 3 * 60 * 1000  # 3 minutes in milliseconds
        self.timer.Tick += self.Timer_Tick
        self.timer.Start()
        self.Timer_Tick(self)

    def Timer_Tick(self, sender, e=None):
        self.textBox1.Clear()
        choice = random.choice(images)
        self.label1.Text = self.Answer = choice.replace(".jpg", "")
        t = self.BackgroundImage
        self.BackgroundImage = Image.FromFile(choice)
        if t: t.Dispose()
        self.TopMost = True
        self.Focus()
        self.BringToFront()
        self.speechSynthesizer.Speak(self.Answer)

    def Text_Changed(self, sender, e):
        if e.KeyChar == '`':
            if (txt := sender.Text.lower()) == (ans := self.Answer.lower()): self.Success()
            elif txt == 'exit': Environment.Exit(0)
            else: MessageBox.Show(ans)

    def Success(self):
        self.SendToBack()
        self.TopMost = False

if __name__ == "__main__":
    Application.EnableVisualStyles()
    Application.SetCompatibleTextRenderingDefault(False)

    form = MainForm()
    Application.Run(form)
