-- TODO: Distribute this across several servers, the API rate limits 1 call 
-- every 5 seconds, as such parallelizing those calls would allow for faster
-- scraping

-- TODO: Implement flipN which takes an int and flips the first arugment n times
-- foward

import qualified Control.Monad as Monad
import qualified Network.HTTP as HTTP 
import qualified Network.URI as URI
import qualified Data.Char as Char

data Lang = EN | ES | RU deriving (Show)
data Date = Date { year :: Int, month :: Int, day :: Int } deriving (Show) 

downcase :: String -> String
downcase = map Char.toLower

userAgent :: HTTP.Header
userAgent = HTTP.mkHeader HTTP.HdrUserAgent firefoxOnUbuntu
  where firefoxOnUbuntu = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"

headers :: [HTTP.Header]
headers = [userAgent]

baseTwitterSearchURI :: String -> Maybe URI.URI
baseTwitterSearchURI = parser $ mappend "https://twitter.com/search?q="
  where parser = URI.parseURI . (escapeURIString isUnescapedInURI)

formatTwitterSearchURI :: String -> Maybe Lang -> Maybe Date -> Maybe URI.URI
formatTwitterSearchURI query None None = baseTwitterSearchURI query 
                     | query (Just lang) None = (baseTwitterSearchURI query ++ "&lang" ++ (show lang)
                     | query None (Just date) = (baseTwitterSearchURI query) ++ "&since=" ++ (show date)
                     | query (Just lang) (Just date) = (baseTwitterSearchURI query) ++ "&lang" ++ (show lang) ++ "&since=" ++ (show date)

main :: IO ()
main = 
  getLine 
  >>= return . 
  >>= return . show . (>>= return . (\uri -> HTTP.Request uri HTTP.GET headers "")) 
  >>= putStrLn 

-- simpleHTTP (getRequest "http://www.haskell.org/") >>= fmap (take 100) . getResponseBody
--
-- simpleHTTP (getRequest "http://www.haskell.org/") >>= fmap (take 100) . getResponseBody
--    fetch document and return it (as a 'String'.)
