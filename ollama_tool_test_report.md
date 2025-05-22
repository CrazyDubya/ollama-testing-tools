# Ollama Model Tool Support Analysis Report

Test Date: 2025-05-03 11:47:07

## Summary

- Total models tested: 18
- Models with native tool calling support: 4 (22.2%)
- Models that work with alternative methods: 4
- Models that work through Llama interface: 5

## Basic Tool Calling Support

| Model | Status | Reason/Notes |
|-------|--------|-------------|
| llama3:8b | ❌ Failed | Error during tool call test: registry.ollama.ai/library/llama3:8b does not support tools |
| nomic-embed-text:latest | ❌ Failed | Error during tool call test: "nomic-embed-text:latest" does not support chat |
| qwq:32b | ✅ Success | Successfully used search tool. |
| deepseek-r1:32b | ❌ Failed | Error during tool call test: registry.ollama.ai/library/deepseek-r1:32b does not support tools |
| mistral-small:24b | ✅ Success | Successfully used search tool. |
| llava-phi3:latest | ❌ Failed | Error during tool call test: registry.ollama.ai/library/llava-phi3:latest does not support tools |
| minicpm-v:latest | ❌ Failed | Error during tool call test: registry.ollama.ai/library/minicpm-v:latest does not support tools |
| long-gemma:latest | ❌ Failed | Error during tool call test: registry.ollama.ai/library/long-gemma:latest does not support tools |
| llama3.1:8b | ✅ Success | Successfully used search tool. |
| phi3:14b-medium-128k-instruct-q8_0 | ❌ Failed | Error during tool call test: registry.ollama.ai/library/phi3:14b-medium-128k-instruct-q8_0 does not support tools |
| moondream:latest | ❌ Failed | Error during tool call test: registry.ollama.ai/library/moondream:latest does not support tools |
| llava:latest | ❌ Failed | Error during tool call test: registry.ollama.ai/library/llava:latest does not support tools |
| llama3.2-vision:11b | ❌ Failed | Error during tool call test: registry.ollama.ai/library/llama3.2-vision:11b does not support tools |
| qwen2.5:0.5b | ❌ Failed | No tool calls; composite search fallback executed |
| gemma2:2b | ❌ Failed | Error during tool call test: registry.ollama.ai/library/gemma2:2b does not support tools |
| llama3.2:latest | ✅ Success | Successfully used search tool. |
| gemma2:9b | ❌ Failed | Error during tool call test: registry.ollama.ai/library/gemma2:9b does not support tools |
| bespoke-minicheck:latest | ❌ Failed | Error during tool call test: registry.ollama.ai/library/bespoke-minicheck:latest does not support tools |

## Advanced Testing of Successful Models

### qwq:32b

#### Complex Query Test
- Status: ✅ Success
- Response: <think>

Okay, so I need to compare the populations of Tokyo and New York City and explain why there's a difference. Let me start by recalling what I know about these two cities.

First, Tokyo is the capital of Japan, right? And New York City is in the United States. I think Tokyo might have a much larger population than NYC, but I'm not entirely sure. Wait, maybe it's the other way around? Hmm, let me think again. 

I remember that Tokyo is often cited as one of the most populous cities globall...

#### Multiple Tool Calls Test
- Status: ✅ Success
- Response: <think>
Okay, the user asked for information comparing Tokyo's transportation system with New York's subway, but my search came up empty. Hmm, maybe there was an issue with the query terms? Let me try different keywords like "Tokyo vs NYC transit systems" or "comparison of Tokyo Metro and NYC Subway". Wait, perhaps I should break it down into parts.

First, I know both cities have extensive subways. Tokyo's system is known for its punctuality and efficiency, while New York's has a longer history...

#### Chain of Thought Test
- Status: ❌ Failed
- Reason: Test error: search_web_ddg() got an unexpected keyword argument 'arguments'

### mistral-small:24b

#### Complex Query Test
- Status: ✅ Success
- Response: I don't have real-time data access, but I can provide some general information based on my knowledge up to 2023.

As of 2021:
- Tokyo has a population of approximately 13.9 million people within its city limits.
- New York City has a population of around 8.4 million people within its city limits.

These numbers can vary slightly depending on the source and the year, but generally, Tokyo is more populous than New York City within their respective city limits.

The difference in population can be ...

#### Multiple Tool Calls Test
- Status: ✅ Success
- Response: I don't have real-time data, but I can provide some general information based on my knowledge up until 2023.

Tokyo's transportation system is renowned for its efficiency, cleanliness, and extensive network. It includes a vast array of trains, subways, buses, and even monorails. The Tokyo Metro and Toei Subway systems are the primary subway networks, covering most of the city and connecting to various train lines operated by Japan Railways (JR) and other private companies.

Key features of Tokyo...

#### Chain of Thought Test
- Status: ✅ Success
- Response: The best times to visit Tokyo for mild weather are during spring (March to May) and fall (September to November). During these seasons, the temperatures are pleasant, and you can avoid the extreme heat of summer and the cold of winter.

Tokyo offers a unique blend of traditional culture and modern technology. Here are some key attractions you should consider:

1. **Senso-ji Temple**: Located in Asakusa, this is Tokyo's oldest temple and one of its most significant. It offers a glimpse into Japan...

### llama3.1:8b

#### Complex Query Test
- Status: ✅ Success
- Response: The population of Tokyo is approximately 38 million people, while the population of New York City is around 8.4 million people.

There are several reasons why the population of Tokyo is so much larger than that of New York City:

1. **Urbanization**: Tokyo has been a major urban center for centuries, and its population has grown steadily over time as people from rural areas have moved to the city in search of work and better living conditions.
2. **Economic growth**: Tokyo is one of the world's ...

#### Multiple Tool Calls Test
- Status: ✅ Success
- Response: Tokyo's transportation system is one of the most extensive and efficient in the world, with a comprehensive network of trains, buses, and subways that make getting around the city easy and convenient. Here are some key features of Tokyo's transportation system:

1. **Subway System**: Tokyo has 9 different subway lines operated by three private companies: Tokyo Metro, Toei Subway, and Odakyu Electric Railway. The subway network covers most areas of the city and is known for its punctuality and re...

#### Chain of Thought Test
- Status: ✅ Success
- Response: **Best Time to Visit Tokyo**

Tokyo has a humid subtropical climate with four distinct seasons. The best time to visit for mild weather is during the spring (March to May) or autumn (September to November). These periods offer pleasant temperatures, ranging from 10°C to 20°C (50°F to 68°F), making it ideal for sightseeing.

**Traditional Culture Attractions**

1. **Meiji Shrine**: Dedicated to the deified spirits of Emperor Meiji and his wife, Empress Shoken.
2. **Asakusa Kannon Temple (Senso-ji...

### llama3.2:latest

#### Complex Query Test
- Status: ✅ Success
- Response: Tokyo has a population of approximately 38 million people, while New York City has a population of around 8.4 million people.

The main reason for this difference is that Tokyo is a megacity located in Japan, which is an island nation with limited land area. As a result, the city's population density is extremely high, with many people living in densely populated areas such as Shinjuku and Shibuya.

On the other hand, New York City is a large but not necessarily densely populated city located on...

#### Multiple Tool Calls Test
- Status: ✅ Success
- Response: Tokyo's transportation system is one of the most comprehensive and efficient in the world, with a network of trains, buses, and subways that cover the entire city. The Tokyo Metro, which includes several different lines, is one of the largest subway systems in the world, with over 9 million passengers per day.

Compared to New York's subway system, Tokyo's transportation system has some key differences:

1. Frequency: Trains run more frequently in Tokyo, with trains arriving every few minutes du...

#### Chain of Thought Test
- Status: ✅ Success
- Response: Tokyo is a year-round destination, but the best time to visit for mild weather is during the spring (March to May) or autumn (September to November). These periods offer comfortable temperatures, ranging from 15°C to 25°C (59°F to 77°F), making them ideal for sightseeing.

For traditional culture, you should consider visiting:

1. The Imperial Palace: A large park in the heart of Tokyo that serves as the main residence of the Emperor of Japan.
2. Senso-ji Temple: A historic Buddhist temple in As...

## Alternative Methods for Failed Models

### llama3:8b

#### Direct JSON Method
- Status: ✅ Success
- Response: It looks like I didn't quite hit the mark. Let me try again!

Here's my revised search:

{
  "action": "search",
  "query": "population of Tokyo"
}

Your turn again!

#### Alternate Search Method
- Status: ✅ Success
- Response: A clever question! Unfortunately, it seems that your search didn't yield any actual results. The message you received indicates that no relevant information was found.

As a result, I must inform you that there is no definitive answer to the population of Tokyo in 2025 based on your search results. You may want to try searching for more general information about Tokyo's population or checking official sources such as the Tokyo Metropolitan Government or the United Nations Department of Economic ...

### nomic-embed-text:latest

#### Direct JSON Method
- Status: ❌ Failed
- Reason: Test error: "nomic-embed-text:latest" does not support chat

#### Alternate Search Method
- Status: ❌ Failed
- Reason: Test error: "nomic-embed-text:latest" does not support chat

### deepseek-r1:32b

#### Direct JSON Method
- Status: ❌ Failed
- Reason: No JSON found in response

#### Alternate Search Method
- Status: ✅ Success
- Response: <think>
Okay, so I'm trying to figure out the population of Tokyo in 2025. The user mentioned they searched for "Tokyo population 2025" and got a result saying "No alternative results found." That's a bit confusing because usually, when you search for something like that, you get some numbers or estimates. 

Hmm, maybe the data isn't available yet because 2025 is in the future. Population projections can be tricky since they depend on various factors like birth rates, death rates, migration, and...

### llava-phi3:latest

#### Direct JSON Method
- Status: ❌ Failed
- Reason: No JSON found in response

#### Alternate Search Method
- Status: ✅ Success
- Response: Based on my knowledge cutoff in September 2021, I cannot provide an exact estimate for the population of Tokyo in 2025. However, according to data from various sources such as United Nations and World Bank, the estimated population of Tokyo-Tokyo Metropolitan Area was around 37 million people in 2020.
It's important to note that population estimates are subject to change over time due to factors such as birth rates, death rates, immigration, and emigration. Therefore, it is possible that the pop...

### minicpm-v:latest

#### Direct JSON Method
- Status: ❌ Failed
- Reason: No JSON found in response

#### Alternate Search Method
- Status: ✅ Success
- Response: Based on my knowledge cutoff date of September 2021, I do not have access to current information or future predictions. Therefore, I cannot provide you with an accurate answer about the population of Tokyo in 2025.
However, it's worth noting that population estimates can fluctuate based on various factors such as birth rates, death rates, migration patterns and other demographic trends. It is always best to consult reliable sources or official government statistics for up-to-date information reg...

## Llama3.2 Interface Tests

### llama3:8b

- Status: ✅ Success
- Response: <think>
Okay, let's see what the user is asking here. They want me to act as a tool caller for Llama3:8b. The steps are clear: first, search for Tokyo's 2025 population info, pass that to Llama3, and then report back its analysis.

Hmm, but when I tried searching earlier, there were no results found. That's an issue. Maybe the user expects me to handle this scenario? Since there's no data, I can't proceed as instructed. The previous responses from the assistant mentioned hitting a roadblock with...

### nomic-embed-text:latest

- Status: ✅ Success
- Response: <think>
Okay, the user wants me to act as a tool caller for the nomic-embed-text:latest model. Let me break down their request step by step.

First, they asked me to search for information about Tokyo's population in 2025. I need to perform that search. But when I tried, the response was "No results found." Hmm, maybe there aren't specific forecasts available yet, or the query terms might be too narrow. Maybe Tokyo's population projections are usually part of broader regional or national data? A...

### deepseek-r1:32b

- Status: ✅ Success
- Response: <think>
Okay, let me try to figure out how to approach this. The user wants me to act as a tool caller for the DeepSeek-R1:32B model. The task has three steps: first, search for information about Tokyo's population in 2025; second, pass those results to DeepSeek-R1:32B for analysis; and third, report back what that model said.

Hmm, starting with the first step—searching for Tokyo's population in 2025. Since I don't have access to real-time data or external search capabilities, I need to rely on...

### llava-phi3:latest

- Status: ✅ Success
- Response: <think>
Okay, the user wants me to act as a tool caller for the llava-phi3:latest model. Let me break down their request step by step.

First, they want me to search for information about Tokyo's population in 2025. I need to perform that search. But when I tried, the response was "No results found." Hmm, maybe there aren't specific projections available yet, or the data isn't widely published. Alternatively, perhaps the search tool I used doesn't have access to that information.

Next step is t...

### minicpm-v:latest

- Status: ✅ Success
- Response: <think>
Okay, let me try to figure out how to approach this. The user wants me to act as a tool caller for minicpm-v:latest. The steps they mentioned are first to search for Tokyo's population in 2025, then pass those results to minicpm-v for analysis, and finally report back what minicpm-v said.

First, I need to perform the search for Tokyo's 2025 population. Since I'm the one doing this, maybe I should check reliable sources like government websites or reputable demographic institutions. Howe...

## Recommendations

### Top Tool-Compatible Models
- qwq:32b
- mistral-small:24b
- llama3.1:8b
- llama3.2:latest

### Models That Work With Alternative Methods
- llama3:8b - Works with: Direct JSON, Alternate Search
- deepseek-r1:32b - Works with: Alternate Search
- llava-phi3:latest - Works with: Alternate Search
- minicpm-v:latest - Works with: Alternate Search

### Models That Work Through Llama3.2 Interface
- llama3:8b
- nomic-embed-text:latest
- deepseek-r1:32b
- llava-phi3:latest
- minicpm-v:latest

## Final Verdict and Usage Recommendations

For best tool calling performance, use: **qwq:32b, mistral-small:24b, llama3.1:8b, llama3.2:latest**

For models without native tool support, the following alternative methods work well:
- llama3:8b: Use Direct JSON/Alternate Search method
- deepseek-r1:32b: Use Alternate Search method
- llava-phi3:latest: Use Alternate Search method
- minicpm-v:latest: Use Alternate Search method

Consider using llama3.2 as a tool calling interface for: llama3:8b, nomic-embed-text:latest, deepseek-r1:32b, llava-phi3:latest, minicpm-v:latest
