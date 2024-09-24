export interface apiRequestResponse {
  status: number;
  text: string;
  body: any | {};
}

export const apiRequest = async ({
  url,
  method = "GET",
  headers = {},
  data,
}: {
  url: string;
  method?: string;
  headers?: any;
  data?: any;
}) => {
  try {
    const response = await fetch(url, {
      method,
      headers,
      body: data ? data : undefined,
    });

    if (!response.ok) {
      console.warn(response);
      return {
        status: response.status,
        text: response.statusText,
        body: {},
      };
    }

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      const body = await response.json();
      return {
        status: response.status,
        text: response.statusText,
        body: body,
      };
    }

    return {
      status: response.status,
      text: response.statusText,
      body: {},
    };
  } catch (error) {
    console.error("API request error:", error);
    throw error;
  }
};

export default apiRequest;
