import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import { FileUploader } from "react-drag-drop-files";
import { useCompositeState } from "ds4biz-core";
import { Box, Button, Flex, Heading, Image, Stack } from "@chakra-ui/react";
import urlJoin from "url-join";
import axios from "axios";
const baseURL = import.meta.env.VITE_BASE_URL || "/";

function getDataUrl(file) {
  var reader = new FileReader();
  return new Promise((resolve, reject) => {
    reader.onload = function (e) {
      resolve(e.target.result);
    };
    reader.readAsDataURL(file);
  });
}

const fileTypes = ["JPG", "PNG", "GIF"];

function App() {
  const state = useCompositeState({
    file: null,
    processing: false,
    data: null,
  });
  const handleChange = (file) => {
    state.file = file;
  };

  useEffect(() => {
    if (state.file) {
      getDataUrl(state.file).then((el) => (state.du = el));
      state.data = null;
    }
  }, [state.file]);
  return (
    <Flex direction={"row"} p="8rem" w="100vw" h="100vh">
      <Stack w="50%">
        <Heading>Loko: Handwriting recognition</Heading>
        <FileUploader
          handleChange={handleChange}
          name="file"
          types={fileTypes}
        />
      </Stack>
      <Stack w="50%">
        <Heading size="md">Uploaded image</Heading>
        <Image src={state.du} />
        {state.file && (
          <Button
            colorScheme={"blue"}
            isLoading={state.processing}
            w="10%"
            onClick={(e) => {
              const url = urlJoin(baseURL, "upload");
              var formData = new FormData();
              console.log(url);
              state.processing = true;

              formData.append("file", state.file);
              formData.append("args", new Blob(["{}"]));
              axios
                .post(baseURL, formData, {
                  headers: {
                    "Content-Type": "multipart/form-data",
                  },
                })
                .then((resp) => {
                  console.log(resp.data);
                  state.data = resp.data;
                })
                .finally(() => (state.processing = false));
            }}
          >
            Analyze
          </Button>
        )}
        {state.data && (
          <>
            <Heading size="md">Recognized text</Heading>

            <Box p="10px" border="1px" borderColor={"black"} fontSize={"xl"}>
              {state.data?.msg}
            </Box>
          </>
        )}
      </Stack>
    </Flex>
  );
}

export default App;
