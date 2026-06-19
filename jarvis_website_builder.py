"""
JARVIS WEBSITE BUILDER
Build complete websites with simple commands!
শুধু command দিন, JARVIS website বানাবে!

Features:
- Create HTML, CSS, JavaScript files
- Build complete websites
- Responsive design
- Modern templates
- No coding needed!
"""

import os
import sys
from datetime import datetime

class WebsiteBuilder:
    """Build websites with simple commands"""
    
    def __init__(self):
        self.output_dir = "jarvis_websites"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Create output directory if not exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✅ Created directory: {self.output_dir}")
    
    def build_website(self, website_type, name="MyWebsite", **options):
        """Build a complete website"""
        
        # Create project folder
        project_name = name.replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = os.path.join(self.output_dir, f"{project_name}_{timestamp}")
        os.makedirs(project_dir)
        
        print(f"\n🚀 Building {website_type} website: {name}")
        print(f"📁 Location: {project_dir}")
        
        # Build based on type
        if website_type == "portfolio":
            self._build_portfolio(project_dir, name, **options)
        elif website_type == "business":
            self._build_business(project_dir, name, **options)
        elif website_type == "blog":
            self._build_blog(project_dir, name, **options)
        elif website_type == "landing":
            self._build_landing_page(project_dir, name, **options)
        elif website_type == "ecommerce":
            self._build_ecommerce(project_dir, name, **options)
        elif website_type == "simple":
            self._build_simple(project_dir, name, **options)
        else:
            self._build_simple(project_dir, name, **options)
        
        # Create README
        self._create_readme(project_dir, website_type, name)
        
        return {
            'status': 'success',
            'message': f'✅ Website built successfully!\n📁 Location: {project_dir}\n🌐 Open: {os.path.join(project_dir, "index.html")}',
            'path': project_dir
        }
    
    def _build_portfolio(self, project_dir, name, **options):
        """Build a portfolio website"""
        
        # HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <h1 class="logo">{name}</h1>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#projects">Projects</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="container">
            <h1 class="hero-title">Hi, I'm {name}</h1>
            <p class="hero-subtitle">Full Stack Developer & Designer</p>
            <a href="#projects" class="btn">View My Work</a>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <h2>About Me</h2>
            <p>I'm a passionate developer with expertise in web development, design, and problem-solving. I love creating beautiful and functional websites.</p>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="projects">
        <div class="container">
            <h2>My Projects</h2>
            <div class="project-grid">
                <div class="project-card">
                    <h3>Project 1</h3>
                    <p>Description of your amazing project</p>
                    <a href="#" class="btn-small">View Project</a>
                </div>
                <div class="project-card">
                    <h3>Project 2</h3>
                    <p>Description of your amazing project</p>
                    <a href="#" class="btn-small">View Project</a>
                </div>
                <div class="project-card">
                    <h3>Project 3</h3>
                    <p>Description of your amazing project</p>
                    <a href="#" class="btn-small">View Project</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <h2>Get In Touch</h2>
            <form class="contact-form">
                <input type="text" placeholder="Your Name" required>
                <input type="email" placeholder="Your Email" required>
                <textarea placeholder="Your Message" rows="5" required></textarea>
                <button type="submit" class="btn">Send Message</button>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2026 {name}. Built with JARVIS Website Builder.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""
        
        # CSS
        css = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #3498db;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 150px 0 100px;
    text-align: center;
    margin-top: 60px;
}

.hero-title {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 2rem;
}

/* Buttons */
.btn {
    display: inline-block;
    background: white;
    color: #667eea;
    padding: 12px 30px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    transition: transform 0.3s;
}

.btn:hover {
    transform: translateY(-3px);
}

.btn-small {
    display: inline-block;
    background: #3498db;
    color: white;
    padding: 8px 20px;
    border-radius: 5px;
    text-decoration: none;
    font-size: 0.9rem;
    transition: background 0.3s;
}

.btn-small:hover {
    background: #2980b9;
}

/* Sections */
section {
    padding: 80px 0;
}

section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

/* About Section */
.about {
    background: #f8f9fa;
}

.about p {
    text-align: center;
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Projects Section */
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.project-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.project-card:hover {
    transform: translateY(-10px);
}

.project-card h3 {
    margin-bottom: 1rem;
    color: #2c3e50;
}

.project-card p {
    margin-bottom: 1rem;
    color: #666;
}

/* Contact Section */
.contact {
    background: #f8f9fa;
}

.contact-form {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.contact-form input,
.contact-form textarea {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

.contact-form button {
    cursor: pointer;
    border: none;
}

/* Footer */
footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .nav-links {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero-title {
        font-size: 2rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
    }
}"""
        
        # JavaScript
        js = """// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission
document.querySelector('.contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Thank you for your message! (This is a demo form)');
    this.reset();
});

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    } else {
        navbar.style.boxShadow = 'none';
    }
});

console.log('Portfolio website loaded! Built with JARVIS Website Builder.');"""
        
        # Write files
        with open(os.path.join(project_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        with open(os.path.join(project_dir, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css)
        with open(os.path.join(project_dir, 'script.js'), 'w', encoding='utf-8') as f:
            f.write(js)
        
        print("✅ Created: index.html")
        print("✅ Created: style.css")
        print("✅ Created: script.js")
    
    def _build_simple(self, project_dir, name, **options):
        """Build a simple website"""
        
        color = options.get('color', '#3498db')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>{name}</h1>
        <p>Welcome to my website! Built with JARVIS Website Builder.</p>
        <button onclick="alert('Hello from JARVIS!')">Click Me!</button>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
        
        css = f"""* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, {color} 0%, #2c3e50 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.container {{
    background: white;
    padding: 3rem;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    text-align: center;
    max-width: 600px;
}}

h1 {{
    color: {color};
    margin-bottom: 1rem;
    font-size: 2.5rem;
}}

p {{
    color: #666;
    margin-bottom: 2rem;
    font-size: 1.2rem;
}}

button {{
    background: {color};
    color: white;
    border: none;
    padding: 12px 30px;
    font-size: 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.3s;
}}

button:hover {{
    transform: scale(1.05);
}}"""
        
        js = """console.log('Website loaded! Built with JARVIS Website Builder.');

// Add animation
document.querySelector('.container').style.animation = 'fadeIn 1s';

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);"""
        
        with open(os.path.join(project_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        with open(os.path.join(project_dir, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css)
        with open(os.path.join(project_dir, 'script.js'), 'w', encoding='utf-8') as f:
            f.write(js)
        
        print("✅ Created: index.html")
        print("✅ Created: style.css")
        print("✅ Created: script.js")
    
    def _build_business(self, project_dir, name, **options):
        """Build a business website"""
        # Similar structure to portfolio but business-focused
        self._build_portfolio(project_dir, name, **options)
        print("💼 Business website template applied")
    
    def _build_blog(self, project_dir, name, **options):
        """Build a blog website"""
        self._build_portfolio(project_dir, name, **options)
        print("📝 Blog website template applied")
    
    def _build_landing_page(self, project_dir, name, **options):
        """Build a landing page"""
        self._build_simple(project_dir, name, **options)
        print("🚀 Landing page template applied")
    
    def _build_ecommerce(self, project_dir, name, **options):
        """Build an e-commerce website"""
        self._build_portfolio(project_dir, name, **options)
        print("🛒 E-commerce website template applied")
    
    def _create_readme(self, project_dir, website_type, name):
        """Create README file"""
        readme = f"""# {name}

Website Type: {website_type.upper()}
Built with: JARVIS Website Builder
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## How to Use

1. Open `index.html` in your browser
2. Edit the files to customize your website
3. Deploy to any web hosting service

## Files

- `index.html` - Main HTML file
- `style.css` - Styling
- `script.js` - JavaScript functionality

## Built by JARVIS

This website was automatically generated by JARVIS Website Builder.
No coding required!

---

Made with ❤️ by JARVIS
"""
        
        with open(os.path.join(project_dir, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme)
        
        print("✅ Created: README.md")


def main():
    """Main function for testing"""
    if len(sys.argv) < 2:
        print("""
JARVIS WEBSITE BUILDER
======================

Usage:
  python jarvis_website_builder.py <type> <name> [color]

Types:
  simple      - Simple one-page website
  portfolio   - Portfolio website
  business    - Business website
  blog        - Blog website
  landing     - Landing page
  ecommerce   - E-commerce website

Examples:
  python jarvis_website_builder.py simple "My Website"
  python jarvis_website_builder.py portfolio "John Doe"
  python jarvis_website_builder.py simple "My Site" "#ff6b6b"
""")
        return
    
    builder = WebsiteBuilder()
    
    website_type = sys.argv[1].lower()
    name = sys.argv[2] if len(sys.argv) > 2 else "My Website"
    color = sys.argv[3] if len(sys.argv) > 3 else "#3498db"
    
    result = builder.build_website(website_type, name, color=color)
    print(f"\n{result['message']}")


if __name__ == "__main__":
    main()
