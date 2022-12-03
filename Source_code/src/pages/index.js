import { useEffect } from 'react';
import Head from 'next/head';
import { gtm } from '../lib/gtm';
import Search from './hotel/search'


const Home = () => {
  useEffect(() => {
    gtm.push({ event: 'page_view' });
  }, []);

  return (
    <>
      <Head>
        <title>
          EBW Hotel Analysis
        </title>
      </Head>
      <main>
        <Search/>
      </main>
    </>
  );
};



export default Home;
