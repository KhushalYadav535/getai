# GetAI Life - Quick Reference Guide

## 🚀 Quick Start Commands

### Setup:
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Redis (in separate terminal)
redis-server

# Run server
python manage.py runserver
```

### Common Commands:
```bash
# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Create new app
python manage.py startapp app_name

# Django shell
python manage.py shell

# Check project
python manage.py check
```

---

## 📁 Important Files और Locations

### Configuration:
- `config/settings.py` - Main settings
- `config/urls.py` - URL routing
- `requirements.txt` - Dependencies
- `.env` - Environment variables

### Models:
- `scrap_data/models.py` - Data, Category, Tags, News, Research models
- `users/models.py` - User, EmailVerification models

### Views:
- `scrap_data/views.py` - Tools listing, scraping views
- `users/views.py` - Authentication views
- `app_modules/llm/views.py` - Chatbot APIs

### Templates:
- `templates/home.html` - Homepage
- `templates/news.html` - News page
- `templates/research.html` - Research page
- `templates/auth/login.html` - Login page

### Static Files:
- `staticfiles/css/style.css` - Main CSS
- `staticfiles/js/custom.js` - Main JavaScript

---

## 🔌 API Endpoints

### Chatbot APIs:
```
POST /api/v1/llm/start-chat/
POST /api/v1/llm/text-generation/
POST /api/v1/llm/chaining/
POST /api/v1/llm/agent-text-generation/
```

### Other APIs:
```
POST /image - Profile picture generator
POST /add-bookmark/<id>/ - Add bookmark
GET /bookmark/ - View bookmarks
```

### Web Pages:
```
/ - Homepage (Tools listing)
/news/ - News page
/research/ - Research page
/submit/ - Tool submission
/login/ - Login page
/register/ - Registration page
/admin/ - Admin panel
```

---

## 🗄️ Database Models Quick Reference

### Data Model:
```python
- title (CharField)
- category (ForeignKey)
- tag (ManyToManyField)
- description (TextField)
- image (FileField)
- webpage (CharField)
- is_featured (BooleanField)
- click_count (PositiveIntegerField)
```

### User Model:
```python
- email (EmailField) - Unique
- username (CharField)
- auth_provider (CharField) - google/email
- is_verify (BooleanField)
```

### Category Model:
```python
- name (CharField)
- image (FileField)
```

### News Model:
```python
- title (CharField)
- description (TextField)
- image (FileField)
- webpage (CharField)
- click_count (PositiveIntegerField)
```

### Research Model:
```python
- title (CharField)
- subject (TextField)
- webpage (CharField)
- click_count (PositiveIntegerField)
```

---

## 🔑 Environment Variables

### Required:
```
DEBUG=True
OPENAI_API_KEY=your_api_key_here
```

### Optional (for PostgreSQL):
```
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
DB_HOST=localhost
```

### Email (SMTP):
```
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_password
```

---

## 🎨 Frontend Components

### Main Sections:
1. **Header** - Navigation, login/logout
2. **Banner** - Homepage banner
3. **Tools Section** - Tools listing
4. **Filters** - Category, search, tags
5. **Footer** - Footer information

### JavaScript Functions:
- `bookmarkItem(itemID, isBookmarked)` - Bookmark functionality
- `selectcat()` - Category selection
- Infinite scroll - Waypoints.js

### CSS Classes:
- `.infinite-container` - Infinite scroll container
- `.otrOpt_bx` - Tool card
- `.filterOtr_bx` - Filter section
- `.bookmark` - Bookmark button

---

## 🤖 Chatbot Configuration

### Healthcare Chatbot:
- Model: GPT-3.5-turbo
- Temperature: 1.0
- Max Tokens: 250
- Cache Key: `HEALTHCARE_{user_id}`

### Finance Chatbot:
- Model: GPT-3.5-turbo
- Temperature: 1.0
- Max Tokens: 250
- Cache Key: `FINANCE_{user_id}`

### Chatbot Flow:
1. User starts chat → `StartChatAPIView`
2. System creates initial prompt
3. AI responds → Response cached
4. User sends message → `TextGenerationAPIView`
5. Previous history fetched from cache
6. New response generated
7. Updated history cached

---

## 🔐 Authentication Flow

### Registration:
1. User enters email and password
2. User account created (is_verify=False)
3. Verification email sent
4. User clicks verification link
5. Account verified (is_verify=True)

### Login:
1. User enters email/username and password
2. System authenticates
3. If email verified → Login successful
4. If email not verified → Verification required

### Google OAuth:
1. User clicks "Continue with Google"
2. Google authentication
3. Account created/updated
4. User logged in

---

## 📊 Data Flow

### Tools Listing:
1. User visits `/`
2. `DataListView` fetches Data objects
3. Filters applied (category, search, tag)
4. Paginated results (40 per page)
5. Rendered in template

### Bookmark:
1. User clicks bookmark
2. AJAX request to `/add-bookmark/<id>/`
3. Favourite model updated
4. Response returned

### Chatbot:
1. User starts chat
2. Initial prompt created
3. OpenAI API called
4. Response cached in Redis
5. Response returned to user

---

## 🐛 Common Issues और Solutions

### Issue: Redis not running
**Solution**: Start Redis server
```bash
redis-server
```

### Issue: OpenAI API key missing
**Solution**: Add to `.env` file
```
OPENAI_API_KEY=your_api_key_here
```

### Issue: Database migrations not run
**Solution**: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic
```

### Issue: Email not sending
**Solution**: Check SMTP settings in `settings.py`

### Issue: Chatbot not working
**Solution**: 
1. Check Redis is running
2. Check OpenAI API key
3. Check cache configuration

---

## 🔧 Development Tips

### Debugging:
- Use `print()` statements
- Use Django debug toolbar
- Check browser console
- Check server logs

### Testing:
- Write unit tests
- Write integration tests
- Test API endpoints
- Test user flows

### Performance:
- Use Redis caching
- Optimize database queries
- Use pagination
- Minimize API calls

### Security:
- Never commit `.env` file
- Use environment variables
- Validate user input
- Use CSRF protection
- Hash passwords

---

## 📝 Code Standards

### Python:
- Follow PEP 8
- Use meaningful variable names
- Add comments
- Write docstrings

### Django:
- Use class-based views
- Use Django ORM
- Follow Django best practices
- Use migrations

### Frontend:
- Use semantic HTML
- Use Bootstrap classes
- Keep JavaScript organized
- Minimize CSS

---

## 🎯 Task Checklist

### Adding New Feature:
- [ ] Plan feature
- [ ] Update models (if needed)
- [ ] Create migrations
- [ ] Create views
- [ ] Create URLs
- [ ] Create templates
- [ ] Write tests
- [ ] Update documentation

### Fixing Bug:
- [ ] Reproduce bug
- [ ] Identify root cause
- [ ] Fix bug
- [ ] Write test
- [ ] Test fix
- [ ] Update documentation

### Deploying:
- [ ] Run tests
- [ ] Check migrations
- [ ] Collect static files
- [ ] Update environment variables
- [ ] Backup database
- [ ] Deploy code
- [ ] Verify deployment

---

## 📚 Useful Resources

### Documentation:
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- OpenAI: https://platform.openai.com/docs
- LangChain: https://python.langchain.com/
- Bootstrap: https://getbootstrap.com/

### Tools:
- Django Admin: `/admin/`
- Django Shell: `python manage.py shell`
- Redis CLI: `redis-cli`
- PostgreSQL: `psql`

---

## 🆘 Emergency Contacts

### Technical Issues:
- Check documentation
- Check logs
- Check GitHub issues
- Contact senior developer

### Server Issues:
- Check server status
- Check database connection
- Check Redis connection
- Check API keys

---

## ✅ Daily Checklist

### Morning:
- [ ] Check server status
- [ ] Check error logs
- [ ] Check user feedback
- [ ] Plan day's work

### During Day:
- [ ] Code changes
- [ ] Test changes
- [ ] Update documentation
- [ ] Review code

### Evening:
- [ ] Commit changes
- [ ] Push to repository
- [ ] Update tasks
- [ ] Plan next day

---

## 🎓 Learning Resources

### For Beginners:
- Python basics
- Django tutorial
- HTML/CSS/JavaScript basics
- Database concepts

### For Intermediate:
- Django advanced
- REST API development
- Database optimization
- Caching strategies

### For Advanced:
- AI/ML integration
- Performance optimization
- Security best practices
- Scalability

---

**Keep this guide handy for quick reference! 🚀**

