# Administrator Guide

This guide covers administrative features for managing the Enterprise Support Assistant, including user management, analytics monitoring, and system maintenance.

## Admin Access

### Logging In as Administrator

1. **Use admin credentials** to log in (default: `john.doe` / `password123`)
2. **Admin button appears** in the navigation bar for users with admin privileges
3. **Click Admin** to access the analytics dashboard

### Admin Dashboard Overview

The admin dashboard provides comprehensive insights into system usage and performance across several key areas.

## Analytics Dashboard

### Usage Overview

**Total Queries**: Overall system usage metrics
- Total number of questions asked
- Unique active users
- Query volume trends over time

**User Engagement Metrics**:
- Daily active users
- Average session duration
- Most active departments
- Peak usage times

### Department Analytics

**Usage by Department**:
- HR: Policy and benefits questions
- IT: Technical support and security queries  
- Finance: Expense and financial policy questions
- Marketing: Brand guidelines and procedures
- General: Mixed organizational queries

**Department Insights**:
- Which departments use the system most frequently
- Common question patterns by department
- Response effectiveness per department

### Query Analysis

**Query Categories**:
- **HR & Benefits**: Time off, health insurance, employee policies
- **IT & Security**: Technical procedures, security protocols, software policies
- **Finance**: Expense reports, budget policies, financial procedures
- **General Policies**: Company-wide procedures and guidelines
- **Other**: Miscellaneous or uncategorized queries

**Popular Queries**:
- Most frequently asked questions
- Trending topics over time
- Seasonal query patterns (e.g., benefits enrollment periods)

### Document Analytics

**Document Access Patterns**:
- Most referenced documents
- Document popularity rankings
- Unused or rarely accessed documents
- Document access frequency over time

**Content Performance**:
- Which documents provide the most helpful responses
- Documents that may need updates or clarification
- Gap analysis for missing documentation

### Performance Metrics

**Response Time Analysis**:
- Average response time per query
- Response time trends over time
- Performance bottlenecks identification

**System Health**:
- Error rates and types
- API usage and limits
- System availability metrics

**Quality Metrics**:
- Source attribution accuracy
- Document relevance scoring
- User interaction patterns

## User Management

### Adding New Users

Edit `user_data.json` to add new employees:

```json
{
  "employees": {
    "new.employee": {
      "employee_id": "EMP999",
      "password_hash": "sha256_hashed_password",
      "first_name": "New",
      "last_name": "Employee",
      "department": "Department",
      "position": "Job Title",
      "is_admin": false
    }
  },
  "sessions": {}
}
```

### Managing Existing Users

**Update User Information**:
- Modify department assignments
- Change job titles or positions
- Update admin privileges

**Reset Passwords**:
1. Generate new password hash using Python:
   ```python
   import hashlib
   password = "new_password"
   hash_value = hashlib.sha256(password.encode()).hexdigest()
   ```
2. Update the `password_hash` field in `user_data.json`

**Deactivate Users**:
- Remove user entry from `user_data.json`
- Clear any active sessions for the user

### Admin Privileges

**Grant Admin Access**:
- Set `"is_admin": true` in user data
- Admin users can access analytics dashboard
- Admin users see additional navigation options

**Revoke Admin Access**:
- Set `"is_admin": false` in user data
- User loses access to admin features immediately

## Document Management

### Adding New Documents

1. **Upload to documents folder**:
   ```bash
   cp new_policy.pdf documents/
   ```

2. **Verify format support**:
   - Supported: TXT, PDF, DOCX, DOC, RTF
   - Maximum recommended file size: 10MB per document

3. **Test document processing**:
   - Restart the application to refresh document index
   - Ask test questions to verify content is accessible

### Managing Existing Documents

**Update Documents**:
- Replace files in the documents folder
- Restart application to reload updated content
- Monitor analytics for impact on query responses

**Remove Documents**:
- Delete files from documents folder
- Restart application to update index
- Update related policies or procedures as needed

**Document Best Practices**:
- Use clear, descriptive filenames
- Keep documents up-to-date with current policies
- Organize by department or topic for easier management
- Regular review and cleanup of outdated content

## System Monitoring

### Performance Monitoring

**Response Time Tracking**:
- Monitor average response times via dashboard
- Investigate spikes or degradation in performance
- Optimize document processing if needed

**API Usage Monitoring**:
- Track Claude API usage against limits
- Monitor costs and usage patterns
- Plan for scaling if usage increases

**Error Monitoring**:
- Review error logs regularly
- Investigate authentication failures
- Monitor document processing errors

### Usage Pattern Analysis

**Peak Usage Times**:
- Identify busy periods for capacity planning
- Understand when employees most need support
- Plan maintenance windows during low usage

**Content Gap Analysis**:
- Identify frequently asked questions without good document coverage
- Review "no relevant documents found" scenarios
- Plan content creation or policy updates

### Security Monitoring

**Session Management**:
- Monitor active sessions
- Review login patterns for anomalies
- Ensure proper session cleanup

**Access Patterns**:
- Review admin access logs
- Monitor for unusual query patterns
- Ensure appropriate use of system resources

## Maintenance Tasks

### Regular Maintenance

**Daily Tasks**:
- Review error logs
- Monitor system performance metrics
- Check API usage levels

**Weekly Tasks**:
- Analyze usage analytics for trends
- Review most popular queries for content gaps
- Update documents as needed

**Monthly Tasks**:
- Full system backup (user data, documents, analytics)
- Review user access and permissions
- Performance optimization review
- Update documentation as needed

### System Updates

**Application Updates**:
1. Backup current system and data
2. Test updates in development environment
3. Schedule maintenance window
4. Deploy updates and verify functionality
5. Monitor for issues post-deployment

**Document Updates**:
1. Coordinate with policy owners (HR, IT, etc.)
2. Replace outdated documents
3. Test query responses with updated content
4. Communicate changes to users if significant

### Backup and Recovery

**Data Backup**:
- User authentication data (`user_data.json`)
- Analytics and usage data
- Company documents
- Application configuration

**Recovery Procedures**:
1. Restore from backup files
2. Verify user access functionality
3. Test document processing
4. Validate analytics data integrity

## Troubleshooting

### Common Admin Issues

**Users Can't Log In**:
- Check user credentials in `user_data.json`
- Verify password hashes are correct
- Clear any stuck sessions

**Poor Response Quality**:
- Review document relevance in analytics
- Check for outdated or conflicting information
- Consider document organization improvements

**Performance Issues**:
- Monitor API response times
- Check document processing efficiency
- Review system resource usage

**Analytics Not Updating**:
- Verify analytics logging is functioning
- Check for data corruption in analytics storage
- Restart application if needed

### Advanced Troubleshooting

**Debug Mode**:
```python
# Add to web_app.py for detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

**System Health Checks**:
1. Test API connectivity
2. Verify document folder accessibility
3. Check user data file integrity
4. Validate session management

**Performance Optimization**:
- Implement caching for frequently accessed documents
- Optimize document processing algorithms
- Consider database migration for high-volume usage

## Best Practices

### System Administration

1. **Regular Monitoring**: Check analytics dashboard weekly
2. **Proactive Maintenance**: Update documents before they become outdated
3. **User Training**: Ensure users know how to get the most from the system
4. **Security First**: Regular password updates and access reviews
5. **Documentation**: Keep admin procedures documented and current

### Content Management

1. **Quality Control**: Regularly review and update company documents
2. **Relevance**: Remove outdated policies and procedures
3. **Accessibility**: Ensure documents are in supported formats
4. **Organization**: Maintain logical document naming and structure
5. **Version Control**: Track document changes and updates

### User Support

1. **Training Materials**: Provide user guides and training sessions
2. **Feedback Collection**: Regular surveys on system usefulness
3. **Issue Resolution**: Quick response to user problems
4. **Usage Promotion**: Highlight valuable features and capabilities
5. **Change Communication**: Notify users of significant updates

## Support and Resources

For additional support:

1. **Technical Issues**: Review system logs and error messages
2. **Feature Requests**: Document requirements for future development
3. **Integration Needs**: Plan for connections with other enterprise systems
4. **Scaling Requirements**: Monitor usage growth and plan capacity
5. **Training Resources**: Develop organization-specific user guides