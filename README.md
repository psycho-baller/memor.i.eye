# Memor.i.eye

You can find the figma prototype video [here](https://drive.google.com/drive/folders/18BWsGO7xVq2fXZJZuj_EfcXJXkyAHBgC?usp=sharing)

## Inspiration

Memories are special to us but in often situations we are faced with the dilemma to record the moments that are special vs fully enjoying them. This gave us the inspiration to build memor.i.eye glasses which capture the moments that are special and are worth re-visiting at some point in the future.

## What it does

- In contrast to automatic cameras or smartphones, we unobtrustively capture and curate photos of the moments in which you first meet new people after placing your gaze on them and when they evoke positive emotions. These are stored on a personal website account where the user can see a catalog of all their essential memories.

## How we built it

- We use signal processing techniques to monitor how eye gaze varies over time through the variance of the running timesteps' eye gaze coordinates. We classify a moment as a "fixation" when one is paying significant attention to a new human face with positive emotions.

## Challenges we ran into

- Determining an appropriate and meaningful custom measure of gaze "fixation", which we defined to be a moment in which the variance of the gaze position is sufficiently small.

## Accomplishments that we're proud of

- It was a lot of fun researching perceptual models and how we could use the glasses to capture the correct memories as they happened
- Building a functional MVP to capture pictures by gaze duration and fixation alongside emotion tracking to further use ML Algorithms to classify these images

## What we learned

- ML embeddings
- Adhawk device + the initial learning curve to exhaust opportunities and ideas
- Using API to connect the frontend(NextJS and the website) and the backend(Python: flask, openCV, ad-hawk, cockroachDB, co.here) of the project
- Thinking in the perspective of the consumer
- Teamwork and effective communication
- Planning and structuring our tasks that ultimately created this big web app in so little time

## What's next for memor.i.eye

- [ ] Improve the signal processing used to determine when it is appropriate to take a picture such as by using pupil dilation technique.
- [ ] Add a feature where you can explicitly choose to take pictures from the glasses by doing a certain blinking action or saying a certain phrase.
- [ ] add image to text translation (AI) where each image is given a caption
- [ ] implement the search bar to search for images by the caption generated from the AI
- [ ] phone compatibility when viewing the images
