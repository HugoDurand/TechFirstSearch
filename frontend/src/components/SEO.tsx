import React from 'react';
import { Platform } from 'react-native';
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  canonicalUrl?: string;
  imageUrl?: string;
  article?: {
    publishedDate: string;
    author?: string;
    source: string;
    tags?: string[];
  };
}

export const SEO: React.FC<SEOProps> = ({
  title,
  description,
  canonicalUrl,
  imageUrl,
  article,
}) => {
  if (Platform.OS !== 'web') {
    return null;
  }

  const fullTitle = `${title} | TechFirstSearch`;
  const siteUrl = 'https://techfirstsearch.com';
  const defaultImage = `${siteUrl}/og-image.png`;

  const jsonLd = article ? {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    description: description,
    image: imageUrl || defaultImage,
    datePublished: article.publishedDate,
    author: {
      '@type': 'Person',
      name: article.author || article.source,
    },
    publisher: {
      '@type': 'Organization',
      name: 'TechFirstSearch',
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/logo.png`,
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': canonicalUrl || siteUrl,
    },
    keywords: article.tags?.join(', '),
  } : {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'TechFirstSearch',
    description: description,
    url: siteUrl,
  };

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      
      {/* Canonical URL - points to original source for articles */}
      {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}
      
      {/* Open Graph */}
      <meta property="og:type" content={article ? 'article' : 'website'} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={imageUrl || defaultImage} />
      <meta property="og:site_name" content="TechFirstSearch" />
      {canonicalUrl && <meta property="og:url" content={canonicalUrl} />}
      
      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={imageUrl || defaultImage} />
      
      {/* Article specific */}
      {article && (
        <>
          <meta property="article:published_time" content={article.publishedDate} />
          {article.author && <meta property="article:author" content={article.author} />}
          {article.tags?.map((tag, i) => (
            <meta key={i} property="article:tag" content={tag} />
          ))}
        </>
      )}
      
      {/* JSON-LD Structured Data */}
      <script type="application/ld+json">
        {JSON.stringify(jsonLd)}
      </script>
    </Helmet>
  );
};

export const HomeSEO: React.FC = () => {
  if (Platform.OS !== 'web') {
    return null;
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'TechFirstSearch',
    description: 'Curated tech news, AI research papers, and programming tutorials from 69+ trusted sources',
    url: 'https://techfirstsearch.com',
    potentialAction: {
      '@type': 'SearchAction',
      target: 'https://techfirstsearch.com/search?q={search_term_string}',
      'query-input': 'required name=search_term_string',
    },
  };

  return (
    <Helmet>
      <title>TechFirstSearch - Tech News & AI Research Aggregator</title>
      <meta 
        name="description" 
        content="Stay updated with the latest tech news, AI research papers, machine learning tutorials, and programming articles from 69+ trusted sources including ArXiv, Hacker News, and top tech blogs." 
      />
      <link rel="canonical" href="https://techfirstsearch.com" />
      
      {/* Open Graph */}
      <meta property="og:type" content="website" />
      <meta property="og:title" content="TechFirstSearch - Tech News & AI Research Aggregator" />
      <meta property="og:description" content="Curated tech news, AI research papers, and programming tutorials from 69+ trusted sources" />
      <meta property="og:url" content="https://techfirstsearch.com" />
      <meta property="og:site_name" content="TechFirstSearch" />
      
      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content="TechFirstSearch - Tech News & AI Research Aggregator" />
      <meta name="twitter:description" content="Curated tech news, AI research papers, and programming tutorials from 69+ trusted sources" />
      
      {/* Additional SEO */}
      <meta name="keywords" content="tech news, AI research, machine learning, programming, software development, artificial intelligence, deep learning, neural networks, computer science" />
      <meta name="robots" content="index, follow" />
      
      {/* JSON-LD */}
      <script type="application/ld+json">
        {JSON.stringify(jsonLd)}
      </script>
    </Helmet>
  );
};

