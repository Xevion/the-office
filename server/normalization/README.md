1. `raw` Directory is almost never edited. It is preserved as a "source of truth" and is only edited when there are flaws in
the original pre-processing.

2. `normalization/truths` acts as a second layer of truth. It is the most basic XML processed file available.

    a. All characters are extracted as 'Speakers', meaning 'Michael' and 'Andy & Dwight' are still valid speakers.
    
    b. Speakers extracted are placed in `speaker_mapping.xml`. This allows misspellings and other such errors to be merged together.
    
    - This step of the process has explicit and direct impact on script data. For example, while we do want
    "Bob Vance Refrigeration Worker #1" and "Bob Vance Refrigeration Worker #2" to show up internally as the same, we do want them to textually
    show differently on the script page.
    
    - Thus, at this stage, we do not merge names of background workers; we only correct mispellings.
    
    c. After this, speakers are translated into a 'identification' file to give short, web-friendly slug identifiers.
    
    - For example, "Michael" becomes `michael`, and "Bob Vance" becomes `bob-vance`.
   
    - Characters will acquire IDs that are most familiar and easy; "Phyllis", while her full name is "Phyllis Vance", will get
        `phyllis`.
    
    - This step of the process is entirely for internal data referencing. From before, the bob vance refrigeration workers
    will all map to the same `bob-vance-refrigeration-worker` internally.
    
    - Additionally, compound speakers (those that do not directly reference their speaker) like `Kevin's Computer` or
    `Kevin and Oscar`, or `Dwight, Kelly, Andy and Pam` will be broken up, and hopefully, be properly
    annotated.
    
    ```xml
    <IdentifierList>
       <Speaker annotated="false">
           <RawText>Phyllis</RawText>
           <Character>phyllis</Character>
       </Speaker>
       <Speaker annotated="true">
           <RawText>Kevin's Computer</RawText>
           <AnnotatedText>{Kevin}'s Computer</AnnotatedText>
           <Characters>
               <Character>kevin</Character>
           </Characters>
       </Speaker>
    </IdentifierList>
   ```
   
   - `<Characters>` elements will be used only for compound speakers. Warnings should show in console in the next step
   when compound speakers are not annotated, or if a `Characters` tag is used while only containing one element.
   If `AnnotatedText` appears in a `Speaker` element's children but `annotated` is false, or

3. `normalization/characters` acts as the character data layer. Here, characters will have their metadata assigned, like whether or not
they are a main, recurring, background or meta character.

    a. Michael, Dwight and Jim are **main** characters. This can be defined by having a very large number of quotes, continued and prolonged
    presence in the show, so and so forth.
    
    b. David Wallace, Bob Vance and Esther are **recurring** characters. While they may play a hefty role in the show, they don't appear enough
    to make it in as a "main character".
    
    c. Captain Jack, Pizza Guy and Bob Vance Refrigeration Worker are **background** characters. These are characters that appear only once
    or make so little impact that it damages the meaning of being a *recurring* character if they were included. The line between a
    *background* character and a *recurring* character may be pretty thin at times, so I anticipate some characters will be difficult to choose.
    
    d. "Everyone" and "None" are **meta** characters (the speakers active won't be searchable, but the quote text will be, as usual).
    This type is reserved for lines that don't really have a character or for more abstract things, or for scene descriptions.

4. `normalization/compiled` is the final stage when all data is *compiled* into one singular dataset.
    
    a. `episodes/{season}-{episode}.xml` contains each episode's data.
     
    ```xml
    <SceneList>
        <Scene>
            <Quote>
                <Speaker>
                    <SpeakerText annotated="true">{Michael}</SpeakerText>
                    <Characters>
                        <Character type="main">michael</Character>
                    </Characters>
                </Speaker>
                <QuoteText>
                    People say I am the best boss. They go, "God we've never worked in a place like this before. You're hilarious."
                    "And you get the best out of us." [shows the camera his WORLD'S BEST BOSS mug] I think that pretty much sums it up.
                    I found it at Spencer Gifts.
                </QuoteText>
            </Quote>
        </Scene>
        <Scene>
            <Quote deleted="true" deletedScene="13">
                <Speaker>
                    <SpeakerText annotated="true">{Dwight} and {Andy}</SpeakerText>
                    <Characters>
                        <Character type="main">dwight</Character>
                        <Character type="main">andy</Character>
                    </Characters>
                </Speaker>
                <QuoteText>
                    [singing] Shall I play for you? Pa rum pump um pum [Imitates heavy drumming] I have no gifts for you.
                    Pa rum pump um pum [Imitates heavy drumming]
                </QuoteText>
            </Quote>
        </Scene>
    </SceneList>
    ```
