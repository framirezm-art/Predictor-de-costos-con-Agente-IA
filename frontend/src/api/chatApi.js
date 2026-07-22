import { axiosClient } from "./axiosClient";

export const chatApi = {
  sendMessage: (message, threadId) =>
    axiosClient.post("/chat", { message, thread_id: threadId }).then((r) => r.data),
};
