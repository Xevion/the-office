import * as functions from "firebase-functions";
import {Storage} from "@google-cloud/storage";

const storage = new Storage();
const bucket = storage.bucket("the-office-episode-data");
const file = bucket.file("data.json");
let quoteData: any = null;

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript

export const surrounding = functions.https.onRequest(
    async (request, response) => {
        const params = {season: -1, episode: -1, scene: -1, quote: -1, radius: -1};
        try {
            params.season = Number(request.query.season);
            params.episode = Number(request.query.episode);
            params.scene = Number(request.query.scene);
            params.quote = Number(request.query.quote);
        } catch (e) {
            response.send("Error processing parameters.").end();
            return;
        }

        // Quote radius
        const minRadius = 1;
        const maxRadius = 5;
        const defaultRadius = 2;
        params.radius = Math.min(Math.max(Number(request.query.radius) || defaultRadius, minRadius), maxRadius);

        // Check that all query parameters were given correctly.
        for (const [k, v] of Object.entries(params)) {
            if (v == null || v == -1 || v == undefined || isNaN(v)) {
                response.send(`Parameter '${k}' was not specified or was fed an invalid integer. (${v})`).end();
                return;
            }
        }

        // Load quote data if not loaded already
        if (quoteData == null) {
            const content = await file.download();
            quoteData = JSON.parse(content[0].toString("utf-8"));
        }

        const sceneData: never[] = quoteData[params.season - 1][params.episode - 1]["scenes"][params.scene - 1].quotes;
        const surrounding = {center: sceneData[params.quote - 1], above: [], below: []};
        const quoteIndex = params.quote - 1;

        if (params.radius > 0) {
            for (let i = 0; i < params.radius; i++) {
                const topIndex = quoteIndex - (i + 1);
                const bottomIndex = quoteIndex + (i + 1);

                if (topIndex >= 0) {
                    surrounding.above.splice(0, 0, sceneData[topIndex]);
                }

                if (bottomIndex < sceneData.length) {
                    surrounding.below.push(sceneData[bottomIndex]);
                }
            }
        }

        response.send({...surrounding, params}).end();
    });
