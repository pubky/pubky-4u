# Pubky 4U: Soevereing "For You" feeds (Research phase👨‍🔬)
Sovereign recommendation engine. Dynamical curation of personalized feeds leveraging Web-of-Trust based algorithms, and global ML collaborative and content based filtering. This system ensures relevant, authentic interactions within the community, optimizing the discovery experience for each user.

## Features 🚀
Envisioned for integration with Pubky's indexing systems like `pubky-nexus`, **pubky-4u** is a research project on cutting-edge recommendation engine that leverages both a Web of Trust (WoT) and lightweight Artificial Intelligence (AI) to deliver transparent and tailored content recommendations. Users can dynamically tune their feeds between purely WoT-driven content to AI-powered suggestions via an intuitive slider interface.

- **WoT Scoring**: Real-time post scoring based on the trust graph queries, considering connections like 'friends of friends' and their interactions.
- **AI Socring**: Utilizes both collaborative filtering and content-based filtering to suggest posts. Techniques include user and post embeddings, e.g, LightFM and feature extraction via TF-IDF.
- **Hybrid Feeds**: Blend WoT and AI scores based on user preference slider, allowing for a highly personalized content stream that are transparent and where user is in ultimate control.

## Roadmap for Hackweek 🛣️
- [ ] Implement WoT graph queries with post scoring capabilities.
- [ ] Research and test collaborative and content-based filtering algorithms in Python.
- [ ] Develop a local CLI demo to showcase sovereign feeds.

## Out of Scope for Hackweek ❌
- [ ] Final implementation in Rust as a module/crate ready for integration.
- [ ] Creation of a full-fledged UI with slider capabilities.

## Why pubky-4u? 🤔
### The Philosophy Behind 4U

This is **my thesis** regarding "recommendations" after considerable reflection:

In all modern social media, "the user is the algorithm," and they tune the algorithm... **unconsciously**! They always get "almost exactly" what they want, with the best UX, as there is no need to click anywhere for curating, filtering, or sorting content. No need to even use a tiny bit of their brain's gray matter to ask themselves "what do I even like?" —it just happens.

However, this approach can be **terrifyingly opaque**: how do we know the feed isn't biased? Or trying to elicit specific emotional responses? It's this black box nature that drives many to distrust and ultimately "we" reject such "algorithms."

In contrast, the "you are the algorithm" motto of Pubky.app means something completely different: you craft your view of the network **consciously**. However, we risk equating **consciously** (you are aware and in control) with **manually** (you do the work), and these two do not necessarily need to be the same. Having control is cool; doing work is not cool. 

Using WoT at the core makes it exciting as it enables a more "conscious" feed without being more "manual" (more control without more work). So this looks like the right stuff to leverage. But it needs to really be leveraged! I believe, on top of it, unless we create "year 2024" tools to craft the feed for the user, the user might quickly give up: woah, sorting, filtering, views. feeds, figuring-it-out—well, that looks like a ton of seemingly upfront work without a clear reward in sight.

Inspiration can be drawn from platforms like Reddit, which has "recency" and "popularity" (their emblematic upvote) yet the default sorting of topics does not seem to use either (it's ML based). Amazon shopping has powerful yet straightforward sorting filtering options, yet: most often we do not want to use it, we want the default ML based feed of items. Discovery is a priority, that's the goal of **4U**. People should be able to discover what they want of the web from Pubky, not the other way around. How will we feel if the good Pubky content is just found because someone shared it on Twitter? (That's how people find good Medium or Stackernews posts).

Ultimately, Pubky's architecture is unique in its capabilities to provide top-tier user experience that is familiar yet revolutionary, where the user truly "owns the identity," "owns the data," and "controls what they see" yet discoverability does not need to be damaged.

## Getting Started 🏁
