const fs = require('fs');
const https = require('https');

const API_KEY = '8fdbca54-49df-4683-85bc-901b13b558b1';
const POST_ID = '695fb27056b3715aeccc1179';

const content = fs.readFileSync('./drafts/sizer-flutter-responsive-ui-fixed.md', 'utf8');

const query = `
mutation UpdatePost($input: UpdatePostInput!) {
  updatePost(input: $input) {
    post {
      id
      title
      url
      updatedAt
    }
  }
}
`;

const variables = {
  input: {
    id: POST_ID,
    title: "Flutter sizer Package: Build Responsive UI the Easy Way",
    contentMarkdown: content,
    settings: {
      isTableOfContentEnabled: true
    }
  }
};

const data = JSON.stringify({
  query,
  variables
});

const options = {
  hostname: 'gql.hashnode.com',
  port: 443,
  path: '/',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': API_KEY,
    'Content-Length': Buffer.byteLength(data)
  }
};

const req = https.request(options, (res) => {
  let body = '';
  res.on('data', (chunk) => body += chunk);
  res.on('end', () => {
    console.log('Response:', JSON.stringify(JSON.parse(body), null, 2));
  });
});

req.on('error', (e) => {
  console.error('Error:', e.message);
});

req.write(data);
req.end();
