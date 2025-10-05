# AI-Powered Instagram Advertisement Agent

An automated Instagram advertisement agent that generates and posts content daily using AI-powered content generation and scheduled posting.

## Features

- **User Interaction**: Collects Instagram credentials and product details via Cerebrus API
- **AI Content Generation**: Uses Gemini API to generate engaging captions and images
- **Duplicate Prevention**: JSON-based storage system prevents content duplication
- **Automated Posting**: Posts to Instagram feed and stories using MCP Instagram Module
- **Scheduled Execution**: Daily posting at 12 AM using cron jobs in Docker
- **Comprehensive Logging**: Full error handling and logging system

## Architecture

```
Cerebrus API → User Input Collection
     ↓
Gemini API → Content Generation (Captions + Images)
     ↓
JSON Storage → History Tracking & Duplicate Prevention
     ↓
MCP Instagram Module → Posting to Feed & Stories
     ↓
Docker Container → Scheduled Execution
```

## Prerequisites

- Docker and Docker Compose
- Instagram Business Account
- Cerebrus API access
- Gemini API access
- Instagram API access (via MCP Instagram Module)

## Quick Start

### 1. Environment Setup

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your actual API credentials:

```env
# Cerebrus API Configuration
CEREBRUS_API_KEY=your_cerebrus_api_key_here
CEREBRUS_BASE_URL=https://api.cerebrus.com

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Instagram API Configuration
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
INSTAGRAM_APP_ID=your_instagram_app_id_here
INSTAGRAM_APP_SECRET=your_instagram_app_secret_here

# Storage Configuration
STORAGE_PATH=./data
```

### 2. Build and Run

```bash
# Build the Docker image
docker-compose build

# Run the container
docker-compose up -d

# Check logs
docker-compose logs -f instagram-agent
```

### 3. Manual Testing

```bash
# Run manual posting (for testing)
docker-compose exec instagram-agent python instagram_agent.py manual

# Check analytics
docker-compose exec instagram-agent python instagram_agent.py analytics

# Cleanup old data
docker-compose exec instagram-agent python instagram_agent.py cleanup 30
```

## Usage

### Daily Automated Posting

The agent automatically runs daily at 12 AM (00:00) to:

1. Collect user input via Cerebrus API
2. Generate AI content using Gemini API
3. Check for duplicates in JSON storage
4. Post to Instagram feed and stories
5. Log all activities

### Manual Operations

```bash
# Manual posting
python instagram_agent.py manual

# Scheduled posting (runs continuously)
python instagram_agent.py schedule

# View analytics
python instagram_agent.py analytics

# Cleanup old data (30 days)
python instagram_agent.py cleanup 30
```

## Configuration

### Content Settings

Edit `config.py` to customize:

- `MAX_CAPTION_LENGTH`: Maximum caption length (default: 2200)
- `MAX_HASHTAGS`: Maximum hashtags per post (default: 30)
- `POST_TIME`: Daily posting time (default: "00:00")

### Storage Settings

The agent uses JSON-based storage in the `./data` directory:

- `prompts_history.json`: Generated prompts history
- `captions_history.json`: Generated captions history
- `images_history.json`: Generated images history
- `posts_history.json`: Posting results history

## API Integration

### Cerebrus API

The agent integrates with Cerebrus API for:

- User credential collection
- Product detail input
- Image upload handling
- Posting preference confirmation

### Gemini API

Uses Google's Gemini API for:

- Caption generation based on product details
- AI image generation
- Hashtag suggestions
- Content analysis

### Instagram API (MCP Module)

Posts content using Instagram's Graph API:

- Feed posts with images and captions
- Story posts
- Account information retrieval
- Post management

## Monitoring and Logs

### Log Files

- Application logs: `instagram_agent.log`
- Cron logs: `/var/log/cron.log`
- Docker logs: `docker-compose logs instagram-agent`

### Health Checks

The container includes health checks that verify:

- Application is running
- API connections are working
- Storage is accessible

## Troubleshooting

### Common Issues

1. **API Key Errors**: Verify all API keys in `.env` file
2. **Instagram Posting Fails**: Check Instagram API permissions
3. **Content Generation Fails**: Verify Gemini API access
4. **Cron Not Running**: Check Docker container logs

### Debug Mode

Enable debug logging by setting the log level in `instagram_agent.py`:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

### Data Recovery

If data is lost, the agent will:

- Recreate storage files automatically
- Continue with new content generation
- Log all recovery actions

## Security Considerations

- Store API keys securely in environment variables
- Use encrypted storage for sensitive data
- Regularly rotate API keys
- Monitor API usage and costs

## Scaling and Performance

### Horizontal Scaling

- Run multiple containers with different schedules
- Use load balancers for API requests
- Implement database storage for large-scale deployments

### Performance Optimization

- Cache generated content
- Implement content batching
- Use CDN for image delivery
- Monitor API rate limits

## Future Enhancements

- **Analytics Dashboard**: Track engagement metrics
- **Multiple Accounts**: Support for multiple Instagram accounts
- **Advanced Scheduling**: Hourly, weekly, custom schedules
- **A/B Testing**: Test different content variations
- **Engagement Tracking**: Monitor likes, comments, story views

## Support

For issues and questions:

1. Check the logs: `docker-compose logs instagram-agent`
2. Verify configuration: `python instagram_agent.py analytics`
3. Test manually: `python instagram_agent.py manual`

## License

This project is licensed under the MIT License - see the LICENSE file for details.