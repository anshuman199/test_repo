

# Manhattan-II


[![Latest Stable Version](http://img.shields.io/github/release/jenssegers/date.svg)](https://packagist.org/packages/jenssegers/date)


markdownRemark(fields: { slug: { eq: $slug } }) {
      htmlAst
      wordCount {
        words
      }
      timeToRead
      frontmatter {
        keywords
      }
      fields {
        title
      }
      parent {
        ... on File {
          mtime
        }
      }
}
