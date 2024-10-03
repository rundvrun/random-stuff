using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace MapleWalking
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        //static Dictionary<string, Image[]> imgs = new Dictionary<string, Image[]>();
        public Form1(string k) : this()
        {
            
            images = new Image[] {
                        Image.FromFile($"../Gifs/{k}_r2l.gif"),
                        Image.FromFile($"../Gifs/{k}_l2r.gif")
                     };
            Init();
            Text = k;
          
        }
    }

}

using System;
using System.Collections.Generic;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

namespace MapleWalking
{
    partial class Form1
    {
        //private const int WM_NCLBUTTONDOWN = 0xA1;
        //private const int HTCAPTION = 0x2;
        [DllImport("User32.dll")]
        private static extern bool ReleaseCapture();
        [DllImport("User32.dll")]
        private static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);

        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Timer timer1;
        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(20, 0);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(144, 131);
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.pictureBox1);
            this.Name = "Form1";
            this.Text = "Maple";

            TransparencyKey = BackColor;
            FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            TopMost = true;
            MaximizeBox = false;
            ShowInTaskbar = false;
            Width = Screen.PrimaryScreen.Bounds.Width;
            Load += Form1_Load;

            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            //
            // timer1
            //
            timer1.Interval = 2;
        }

        #endregion

        #region My Code
        static byte offset = 2, XLeft = 2;
        byte flag = 1; /* 1=L2R, 0=R2L */
        int counter = 0, i = 0;
        static int XRight = Screen.PrimaryScreen.Bounds.Width - 100, offsetY = 2;
        //static OpenFileDialog openner = new OpenFileDialog();
        Image[] images;// = new Image[] {
        //    openner.GetImage("R2L"),
        //    openner.GetImage("L2R")
        //};
        public static Random rd = new Random();
        //static Point pos = new Point(XLeft + rd.Next(Screen.PrimaryScreen.Bounds.Width - 100), 1);
        Point pos_frm = new Point(XLeft + rd.Next(Screen.PrimaryScreen.Bounds.Width - 100), rd.Next(Screen.PrimaryScreen.Bounds.Height - 100));
        static int maxY, minY;
        //string key = string.Empty;
        private void Init()
        {
            //XRight = Width - 50;
            pictureBox1.Tag = true;
            pictureBox1.MouseEnter += (s, e) => {
                Tag = Opacity;
                Opacity = 1;
                pictureBox1.Tag = false;
                TopMost = true;
            };
            pictureBox1.MouseLeave += (s, e) => {
                Opacity = (double)Tag;
                pictureBox1.Tag = true;
            };

            pictureBox1.MouseDown += (s, e) => {
                switch (e.Button)
                {
                    case MouseButtons.Left:
                        ReleaseCapture();
                        SendMessage(Handle, /*WM_NCLBUTTONDOWN*/ 0xA1, /*HTCAPTION*/ 0x2, 0);
                        pos_frm = Location;
                        pos_frm.Y = Math.Min(pos_frm.Y, maxY);
                        pos_frm.Y = Math.Max(pos_frm.Y, minY);
                        break;
                    case MouseButtons.Right:
                        timer1.Stop();
                        Close();
                        if (Form2.frms.Count == 0)
                        {
                            Application.Exit();
                            MessageBox.Show("!");
                        }
                        break;
                    default:
                        break;
                }
            };

            FormClosing += (s, e) => {
                Form2.frms.Remove(this);
                Dispose();
            };

            timer1.Tick += (s, e) =>
            {
                Thread.Sleep(60);
                //if (pictureBox1.Location.X > XRight || pictureBox1.Location.X < XLeft)
                if (Location.X > XRight || Location.X < XLeft)
                    pictureBox1.Image = images[flag ^= 1];
                //if (Location.X > XRight || Location.X < XLeft)
                //pos.X += offset * ((flag | (1 << flag)) - 2); // [(L2R | 1 << L2R)=3 - 2=1]*offset; [(R2L | 1 << R2L)=1 - 2=-1]*offset
                //pos.X += offset * (flag - (1 >> flag)); // flag = 1 => 1 >> flag = 0 => 1 - 0 = 1; flag = 0 => 1 >> flag = 1 => 0 - 1 = -1;
                //var i = rd.Next(-9, 11);
                //pos_frm.Y += i <= -6 ? -offsetY : i >= 6 ? offsetY : 0;
                pos_frm.X += offset * (flag - (1 >> flag));
                if (++i > counter)
                {
                    counter = rd.Next(550);
                    i = rd.Next(counter >> 3);
                    offsetY = -offsetY;
                }
                else
                    pos_frm.Y += offsetY * rd.Next(2);
                
                pos_frm.Y = Math.Min(pos_frm.Y, maxY);
                pos_frm.Y = Math.Max(pos_frm.Y, minY);
                //pictureBox1.Location = pos;
                Location = pos_frm;
                if ((bool)pictureBox1.Tag)
                    Opacity = Math.Max(.75, Math.Min(.85, rd.NextDouble()));
                TopMost = true;
                
            };
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            pictureBox1.Image = images[flag];
            pictureBox1.Height = pictureBox1.Image.Height + 3;
            pictureBox1.Width = pictureBox1.Image.Width + 3;
            Height = pictureBox1.Height + 3;
            Width = pictureBox1.Width + 40;
            Location = pos_frm;
            //pictureBox1.Location = pos;
            timer1.Start();
            //openner.Dispose();
            maxY = Screen.PrimaryScreen.Bounds.Height - pictureBox1.Height / 2;
            minY = -pictureBox1.Height / 3;

        }
        #endregion
    }
}



using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MapleWalking
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form2());
        }
    }

    class Form2 : Form
    {
        static short MaxSpawn = 10;
        public static List<Form1> frms = new List<Form1>();
        
        static List<Thread> threads = new List<Thread>();
        static List<string> c = Directory.GetFiles("../Gifs/", "*_*.gif")
                    .Select(t => t.Replace("_r2l.gif", ""))
                    .Select(t => t.Replace("_l2r.gif", ""))
                    .Distinct()
                    .Select(t => t.Replace("../Gifs/", ""))
                    .ToList();
        public Form2()
        {
            int i = Form1.rd.Next(MaxSpawn) + 1;
            if (i > 0 && i <= MaxSpawn)
            {
                
                for (var ii = 0; ii < i; ++ii)
                {
                    //frms.Add(new Form1(c[rd.Next(c.Count)]));

                    var frm = new Form1(c[Form1.rd.Next(c.Count)]);
                    //frm.ShowDialog();
                    frms.Add(frm);

                    Thread t = new Thread(fm => (fm as Form1).ShowDialog());
                    t.Start(frm);
                    threads.Add(t);
                    //frms[ii].Show();
                }
            }
            Shown += (s, e) => Visible = false;
            ShowInTaskbar = false;

            /*Width = 200;
            Height = 100;
            CenterToScreen();
            var num = new TextBox() { Width = 50, Location = new System.Drawing.Point(0, 0) };
            var btn = new Button() { Text = "Run", Location = new System.Drawing.Point(100, 0) };
            btn.Click += (s, e) =>
            {
                
                short i = 0;
                try
                {
                    Int16.TryParse(num.Text, out i);
                }
                catch (Exception)
                {
                    
                }
                //i = Math.Min(i, MaxSpawn);
                i = (short)Form1.rd.Next(MaxSpawn + 1);
                if (i > 0 && i <= MaxSpawn)
                {
                    Hide();
                    for (var ii = 0; ii < i; ++ii)
                    {
                        //frms.Add(new Form1(c[rd.Next(c.Count)]));

                        var frm = new Form1(c[Form1.rd.Next(c.Count)]);
                        //frm.ShowDialog();
                        frms.Add(frm);

                        Thread t = new Thread(fm => (fm as Form1).ShowDialog());
                        t.Start(frm);
                        threads.Add(t);
                        //frms[ii].Show();
                    }
                }
            };
            Controls.Add(num);
            Controls.Add(btn);*/
        }
    }
}
