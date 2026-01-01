# draft

A draft of my vision for `the-office` project.

## Project Goals

A mobile-friendly, responsive and fast-loading site. Looks good on most devices, and is easy to navigate and read.

Provides access to episode scripts, popular quotes, and character/episode/season information.

Has a fast and simple search interface for finding any quote someone might be looking for.

## Engineering Goals

- Real-time, low latency searching

For the time being, Typesense seems like the best option. With easy Docker-based self-hosting on Railway, it appears to
be the cheapest, fastest, and overall easiest option. Keeping the price down is a priority, and overall it seems like ~$4/month is hard to beat with Railway.
The rest of the options are either incredibly expensive, or would require a lot of engineering effort to re-implement.

As an alternative, I'm also considering in-browser pre-indexed solutions such as FlexSearch and Stork. The benefit of this is that it's far easier to host long-term, and the implementation is simpler overall.

Assuming there are no major complications with in-browser search and pre-built indexes, I think FlexSearch is the overall best option. Since it's a demo, I'm not too worried about performance on low-end devices, and more concerned with the cost of hosting long-term.

- Editable internal data

I already have a lot of data in the `data/` directory from the first iteration of the project. I'm looking for a way to edit the data in a easy, maintainable way.

As I see it, there are a couple of options:

1. A SQL database as the mutable, queryable, living document, which persists to Typesense, and can be exported into JSON as the source of truth within the repository.

   - Requires another service to be running, increasing cost and complexity.
   - More flexible in terms of editing interface, but requires a lot of engineering effort to implement.
   - The ideas and improvements I create here could transfer to a more generic project in the future.
   - Potentially, I could run with Cloudflare D1 as a mostly-idle database, I would fit within the free tier limits, and after initial development, the costs would be nil. I only need SQLite, and low-latency is my biggest concern.

2. The repository itself continues to be the source of truth storing XML or JSON file-based data, and the development server is used to mutate the data on-disk. The production site is statically generated from this.

   - Simpler to implement, requires some effort, and is still somewhat flexible.
   - More effort long-term, but short-term would be more likely to reach the goal of a working site.
   - I really don't like the idea of manually editing XML or JSON files though, and I'm also not sure how I would want to go about editing files with a GUI.

-
